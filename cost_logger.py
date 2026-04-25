import boto3
import json
from datetime import datetime

s3 = boto3.client("s3", region_name="ap-south-1")

BUCKET = "cloudpulse-reports"
KEY = "cost/cost_history.json"


def log_cost(total_cost):

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "cost": total_cost
    }

    try:
        obj = s3.get_object(Bucket=BUCKET, Key=KEY)
        data = json.loads(obj["Body"].read().decode("utf-8"))
    except:
        data = []

    data.append(entry)

    s3.put_object(
        Bucket=BUCKET,
        Key=KEY,
        Body=json.dumps(data, indent=4),
        ContentType="application/json"
    )