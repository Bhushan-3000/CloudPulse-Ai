import boto3
import json
from datetime import datetime

s3 = boto3.client("s3", region_name="ap-south-1")

BUCKET = "cloudpulse-reports"
KEY = "alerts/alerts.json"


def log_alert(instance, cpu, status, message):

    new_alert = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "instance": instance,
        "cpu": cpu,
        "status": status,
        "message": message
    }

    try:
        obj = s3.get_object(Bucket=BUCKET, Key=KEY)
        data = json.loads(obj["Body"].read().decode("utf-8"))
    except:
        data = []

    data.append(new_alert)

    s3.put_object(
        Bucket=BUCKET,
        Key=KEY,
        Body=json.dumps(data, indent=4),
        ContentType="application/json"
    )