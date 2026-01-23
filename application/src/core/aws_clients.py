import boto3
from core.config import REGION

def eventbridge_scheduler_client ():
    return boto3.client("scheduler",region_name=REGION)

