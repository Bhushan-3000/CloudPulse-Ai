import boto3
from datetime import datetime, timedelta

def get_cpu_usage(instance_id):
    cloudwatch = boto3.client('cloudwatch')

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    datapoints = response['Datapoints']

    if not datapoints:
        return 0

    # get latest datapoint
    latest = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]

    return latest['Average']


def get_instance_name(instance_id):
    ec2 = boto3.client('ec2')

    response = ec2.describe_instances(InstanceIds=[instance_id])

    reservations = response['Reservations']
    
    for reservation in reservations:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        return tag['Value']
    
    return "No Name"



def get_all_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()

    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']['Name']

            if state == "running":  # only running instances
                instances.append(instance['InstanceId'])

    return instances


def get_instance_type(instance_id):
    ec2 = boto3.client('ec2')

    response = ec2.describe_instances(InstanceIds=[instance_id])

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            return instance['InstanceType']

    return "unknown"