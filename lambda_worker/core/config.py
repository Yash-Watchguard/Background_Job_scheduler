import os

AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")

JOB_TABLE = os.environ.get("JOB_TABLE", "Job_Records")
LOG_BUCKET = os.environ.get("LOG_BUCKET", "bg-logs-bucket")
