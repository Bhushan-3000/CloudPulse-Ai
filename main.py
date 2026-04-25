from aws_monitor import get_cpu_usage, get_instance_name, get_all_instances
from analyzer import analyze_usage
from ai_explainer import explain
from sns_alerts import send_alert

instances = get_all_instances()

for instance_id in instances:
    cpu = get_cpu_usage(instance_id)
    status = analyze_usage(cpu)
    name = get_instance_name(instance_id)



    # 🚨 SNS ALERT LOGIC (PASTE HERE)
    if status == "underutilized" and cpu < 5:
        send_alert(
            subject="⚠️ CloudPulse Alert: Underutilized Instance",
            message=f"""
Instance: {name}
CPU Usage: {cpu}%
Status: UNDERUTILIZED

Recommendation:
Stop or downgrade to save cost.
"""
        )

    elif status == "moderate":
        send_alert(
            subject="🟡 CloudPulse Alert: Moderate Usage",
            message=f"""
Instance: {name}
CPU Usage: {cpu}%
Status: MODERATE

Recommendation:
Monitor usage closely.
"""
        )

    print("\n-----------------------------")
    print(f"Instance ID: {instance_id}")
    print(f"Instance Name: {name}")
    print(f"CPU Usage: {cpu:.2f}%")
    print(f"Status: {status}")

    if status == "underutilized":
        suggestion = "Stop or downgrade instance"
    elif status == "moderate":
        suggestion = "Monitor usage"
    else:
        suggestion = "Instance is properly utilized"

    print(f"Suggestion: {suggestion}")

    print("\nAI Explanation:")
    explanation = explain(name, cpu, status)
    print(explanation)