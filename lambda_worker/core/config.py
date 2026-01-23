import os

AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")

JOB_TABLE = os.environ["JOB_TABLE"]
LOG_BUCKET = os.environ["LOG_BUCKET"]
