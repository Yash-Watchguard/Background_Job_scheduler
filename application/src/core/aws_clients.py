import boto3
from core.config import REGION

def eventbridge_scheduler_client():
    return boto3.client("scheduler",region_name=REGION)

def get_db():
    return boto3.client('dynamodb',region_name=REGION)