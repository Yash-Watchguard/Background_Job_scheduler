import boto3
from core.config import AWS_REGION

dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)

