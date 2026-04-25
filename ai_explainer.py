import requests

def explain(instance_name, cpu_usage, status):
    prompt = f"""
You are an expert in cloud cost optimization.

Instance Name: {instance_name}
CPU Usage: {cpu_usage}%
Status: {status}

Rules:
- If CPU is low → suggest stopping or downsizing
- If CPU is moderate → suggest monitoring
- If CPU is high → say it is properly utilized and no cost waste

Explain in 2 short lines:
1. Why this status is correct
2. What action should be taken (if any)
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()