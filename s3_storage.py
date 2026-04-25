import boto3
import json
from datetime import datetime

s3 = boto3.client('s3', region_name='ap-south-1')

def upload_report(data, bucket_name):
    filename = f"report-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
    key = f"reports/{filename}"

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )

    return key