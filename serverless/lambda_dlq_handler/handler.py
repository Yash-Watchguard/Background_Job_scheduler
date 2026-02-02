import json
from job_repo import JobRepo
from job_service import JobService

from core.aws_clients import dynamodb
job_repo = JobRepo(dynamodb)

Job_service = JobService(job_repo)

def handler(event, context):
 
    for record in event["Records"]:
        try:
            body = json.loads(record["body"])
            job_id = body["job_id"]

            message_id = record["messageId"]
            execution_id = f"{job_id}#{message_id}"

            Job_service.update_execution_status(job_id,execution_id)

        except Exception as e:
            pass