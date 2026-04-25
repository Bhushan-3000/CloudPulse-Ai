import boto3

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:763997219870:cloudpulse-alerts"

sns = boto3.client("sns", region_name="ap-south-1")

def send_alert(subject, message):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )