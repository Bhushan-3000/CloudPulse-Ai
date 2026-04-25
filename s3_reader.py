import boto3
import json

s3 = boto3.client('s3', region_name='ap-south-1')

def list_reports(bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix="reports/")
    return response.get("Contents", [])

def get_report(bucket_name, key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    data = obj['Body'].read().decode('utf-8')
    return json.loads(data)