import os

REGION = os.getenv("AWS_REGION", "ap-south-1")
JOB_QUEUE_ARN = os.getenv("BG_JOB_QUEUE_ARN","arn:aws:sqs:ap-south-1:344776058261:bg-job-queue")
SCHEDULER_ROLE_ARN = "arn:aws:iam::344776058261:role/EventBridgeSchedulerToSQSRole"
SCHEDULE_GROUP_NAME = os.getenv("SCHEDULE_GROUP_NAME","bg-job-scheduler-group")
TABLE_NAME = os.getenv("DYNAMO_TABLE_NAME", "Job_Records")
algo: str = os.getenv("JWT_ALGORITHM", "HS256")
expiry_time: int = int(os.getenv("JWT_EXPIRY_TIME", "1"))  # 1 hour default
secret_key: str = os.getenv("JWT_SECRET_KEY","yashgoyal123").encode('utf-8')
