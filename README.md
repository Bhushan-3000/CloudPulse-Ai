# ☁️ CloudPulse AI – Cloud FinOps Intelligence Platform

> 🚀 A real-time AWS EC2 monitoring, cost optimization, and AI-powered cloud efficiency dashboard built for modern FinOps workflows.

---

## 🔥 Overview

CloudPulse AI is a **cloud-native FinOps observability platform** that helps engineers and organizations monitor AWS infrastructure in real time, detect cost inefficiencies, and optimize cloud spending using intelligent insights.

It acts as a lightweight alternative to **AWS CloudWatch + Cost Explorer + AI Advisor**, unified into a single dashboard.

---

## ⚡ Key Features

- 📊 Real-time AWS EC2 instance monitoring
- 💰 Automated cloud cost estimation (per instance & total)
- 🚨 Smart AWS SNS alerting system for anomalies
- 📚 S3-based historical report storage & analytics
- 🤖 AI-powered cost optimization recommendations
- 📈 Grafana-style interactive dashboard UI (Streamlit)
- 🔁 Live refresh monitoring system
- 🧠 Intelligent classification (Underutilized / Moderate / Optimal)

---

## 🏗️ Architecture

AWS EC2 → Boto3 Monitoring Layer → Streamlit Dashboard
│
├── S3 → Report Storage
├── SNS → Alert Notifications
└── AI Layer → Cost Optimization Insights


---

## ☁️ AWS Services Used

- **Amazon EC2** → Resource monitoring
- **Amazon S3** → Historical report storage
- **Amazon SNS** → Real-time alert notifications
- **IAM** → Secure access management
- **Boto3 SDK** → AWS integration layer

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 📊
- AWS (EC2, S3, SNS)
- Boto3
- Pandas

---

## 🎯 Project Goal

To design a **cloud-native FinOps intelligence system** that provides real-time visibility into AWS EC2 resource utilization, enables cost optimization, and delivers intelligent insights for improving cloud efficiency.


---

## 🚀 How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/CloudPulse-Ai.git
cd CloudPulse-Ai
```

Install dependencies
```bash
pip install -r requirements.txt
```
Configure AWS
```bash
aws configure
```
Run application
```bash
streamlit run app.py
```

## 💡 Why This Project Matters

Cloud spending is one of the biggest challenges in modern cloud infrastructure.

## CloudPulse AI demonstrates:

-Real-world FinOps engineering
-AWS cloud integration skills
-Observability system design
-Cost optimization intelligence
-AI-assisted decision making

## 🧠 Future Enhancements

-🔥 ML-based cost anomaly detection
-📊 Multi-account AWS support
-🌐 Kubernetes monitoring integration
-📉 Advanced cost forecasting models
-🔐 IAM role-based secure deployment

## 👨‍💻 Author

Bhushan Kumbhar

Cloud & DevOps Engineer | FinOps & AWS Cloud Practitioner | Building Scalable Cloud Systems



## ⭐ If You Like This Project

Give it a ⭐ on GitHub and connect with me for more cloud engineering projects.
