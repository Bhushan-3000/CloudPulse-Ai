import streamlit as st
import pandas as pd
import time
import json
import boto3

from aws_monitor import (
    get_cpu_usage,
    get_instance_name,
    get_all_instances,
    get_instance_type
)

from analyzer import analyze_usage
from ai_explainer import explain
from sns_alerts import send_alert
from alert_logger import log_alert
from cost_logger import log_cost
from s3_reader import list_reports, get_report


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="CloudPulse AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRICING = {
    "t2.micro": 0.0116,
    "t2.small": 0.023,
    "t2.medium": 0.0464
}

BUCKET = "cloudpulse-reports"


# =========================
# SESSION STATE
# =========================
if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = {}


# =========================
# HEADER (CLEAN)
# =========================
st.title("☁️ CloudPulse AI – Cloud FinOps & Observability Platform")
st.caption("Real-time EC2 monitoring, cost optimization insights, and AI-driven cloud efficiency analytics.")


# =========================
# SIDEBAR
# =========================
st.sidebar.header("Controls")
show_ai = st.sidebar.checkbox("Show AI Explanation", value=True)

if st.sidebar.button("🔄 Refresh"):
    st.rerun()


# =========================
# FETCH DATA
# =========================
instances = get_all_instances()
data = []

# =========================
# PROCESS INSTANCES
# =========================
if instances:

    for instance_id in instances:

        cpu = get_cpu_usage(instance_id)
        status = analyze_usage(cpu)
        name = get_instance_name(instance_id)
        instance_type = get_instance_type(instance_id)

        price = PRICING.get(instance_type, 0.02)
        monthly_cost = price * 24 * 30 * 83
        cost = f"₹{int(monthly_cost)}/month"

        # Suggestion
        if status == "underutilized":
            suggestion = "Stop / Downgrade"
        elif status == "moderate":
            suggestion = "Monitor"
        else:
            suggestion = "Optimal"


        # =========================
        # ALERT SYSTEM (COOLDOWN)
        # =========================
        COOLDOWN = 300
        key = instance_id
        last_time = st.session_state.last_alert_time.get(key, 0)

        if time.time() - last_time > COOLDOWN:

            if status == "underutilized" and cpu < 5:

                msg = f"Instance: {name}\nCPU: {cpu}%\nUNDERUTILIZED"

                send_alert("⚠️ CloudPulse Alert", msg)
                log_alert(name, cpu, status, msg)

                st.session_state.last_alert_time[key] = time.time()

            elif status == "moderate":

                msg = f"Instance: {name}\nCPU: {cpu}%\nMODERATE"

                send_alert("🟡 CloudPulse Alert", msg)
                log_alert(name, cpu, status, msg)

                st.session_state.last_alert_time[key] = time.time()


        data.append({
            "Instance Name": name,
            "Instance ID": instance_id,
            "Instance Type": instance_type,
            "CPU Usage (%)": round(cpu, 2),
            "Status": status,
            "Suggestion": suggestion,
            "Estimated Cost": cost
        })


df = pd.DataFrame(data)


# =========================
# KPI ROW (GRAFANA STYLE)
# =========================
st.markdown("## 📊 Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total", len(df))
c2.metric("Underutilized", len(df[df["Status"] == "underutilized"]))
c3.metric("Moderate", len(df[df["Status"] == "moderate"]))
c4.metric("High", len(df[df["Status"] == "high"]) if "high" in df["Status"].values else 0)


# =========================
# TABS (FIX FOR SCROLL ISSUE)
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Monitoring",
    "💰 Cost",
    "🚨 Alerts",
    "📚 History",
    "🔍 Deep Dive"
])


# =========================
# TAB 1 - MONITORING
# =========================
with tab1:

    st.subheader("CPU Utilization")

    def color_status(val):
        if val == "underutilized":
            return "color:red; font-weight:bold"
        elif val == "moderate":
            return "color:orange; font-weight:bold"
        return "color:green; font-weight:bold"

    st.dataframe(df.style.applymap(color_status, subset=["Status"]), use_container_width=True)

    st.bar_chart(df.set_index("Instance Name")["CPU Usage (%)"])


# =========================
# TAB 2 - COST
# =========================
with tab2:

    st.subheader("💰 Cost Overview")

    st.dataframe(df[["Instance Name", "Instance Type", "Estimated Cost"]])

    total_cost = df["Estimated Cost"].str.replace("₹","").str.replace("/month","").astype(float).sum()

    st.metric("Total Monthly Cost", f"₹{int(total_cost)}")

    log_cost(total_cost)


# =========================
# TAB 3 - ALERTS
# =========================
with tab3:

    st.subheader("🚨 Alert History")

    try:
        s3 = boto3.client("s3", region_name="ap-south-1")
        obj = s3.get_object(Bucket=BUCKET, Key="alerts/alerts.json")
        alerts = json.loads(obj["Body"].read().decode("utf-8"))

        alert_df = pd.DataFrame(alerts)

        st.dataframe(alert_df, use_container_width=True)
        st.bar_chart(alert_df["status"].value_counts())

    except:
        st.info("No alerts yet.")


# =========================
# TAB 4 - HISTORY
# =========================
with tab4:

    st.subheader("📚 S3 Reports")

    reports = list_reports(BUCKET)

    if reports:
        selected = st.selectbox("Select Report", [r['Key'] for r in reports[::-1]])

        if selected:
            report_data = get_report(BUCKET, selected)
            hist_df = pd.DataFrame(report_data)

            st.dataframe(hist_df)
            st.bar_chart(hist_df.set_index("Instance Name")["CPU Usage (%)"])
    else:
        st.info("No historical reports.")


# =========================
# TAB 5 - DEEP DIVE (IMPROVED UI)
# =========================
with tab5:

    st.subheader("🔍 Instance Deep Dive")

    for row in data:

        status_color = (
            "🔴 UNDERUTILIZED" if row["Status"] == "underutilized"
            else "🟠 MODERATE" if row["Status"] == "moderate"
            else "🟢 OPTIMAL"
        )

        with st.container():
            st.markdown("---")

            # ===== MAIN CARD =====
            st.markdown(f"""
### ☁️ {row['Instance Name']}

**Status:** {status_color}  
**Instance Type:** `{row['Instance Type']}`  
**CPU Usage:** `{row['CPU Usage (%)']}%`  
**Estimated Cost:** `{row['Estimated Cost']}`
""")

            # ===== QUICK METRICS =====
            c1, c2, c3 = st.columns(3)

            c1.metric("CPU Usage", f"{row['CPU Usage (%)']}%")
            c2.metric("Cost", row["Estimated Cost"])
            c3.metric("Type", row["Instance Type"])

            # ===== AI SECTION (COLLAPSIBLE) =====
            if show_ai:
                with st.expander("🧠 AI Insights", expanded=False):

                    st.write(
                        explain(
                            row["Instance Name"],
                            row["CPU Usage (%)"],
                            row["Status"]
                        )
                    )