from mypy_boto3_dynamodb import DynamoDBClient

import boto3
import os


REGION = os.getenv("AWS_REGION", "ap-south-1")
TABLE_NAME = os.getenv("DYNAMO_TABLE_NAME", "Job_Records")

dynamodb:DynamoDBClient = boto3.client('dynamodb',region_name=REGION)


def get_db() ->DynamoDBClient:
    return dynamodb



