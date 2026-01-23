import boto3
from core.config import AWS_REGION

dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
s3 = boto3.client("s3", region_name=AWS_REGION)
ses = boto3.client("ses", region_name=AWS_REGION)