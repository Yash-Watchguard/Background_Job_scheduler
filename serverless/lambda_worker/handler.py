import json

from repositories.job_repo import JobRepo
from services.email_service import EmailService
from services.execution_logger import ExecutionLogger
from core.aws_clients import s3
from core.config import LOG_BUCKET
from services.job_service import JobService
from models.job_model import JobRecord
from services.log_service import LogService
from enums.execution_status import ExecutionStatus
from datetime import datetime, timezone


job_repo = JobRepo()
log_service: LogService = LogService()
email_service = EmailService()

job_service: JobService = JobService(job_repo)


def handler(event, context):

    for record in event["Records"]:
        execution_logger = ExecutionLogger()

        body = json.loads(record["body"])
        job_id = body["job_id"]
        user_id = body["user_id"]
        message_id = record["messageId"]

        receive_count = int(record["attributes"]["ApproximateReceiveCount"])

        execution_id = f"{job_id}#{message_id}"

        execution_logger.log(
            f"Processing job_id={job_id}, execution_id={execution_id}, attempt={receive_count}"
        )


        job_execution = job_service.get_job_execution(job_id, execution_id)

        if not job_execution:
            job_service.post_job_execution(job_id, execution_id)
            execution_logger.log("Job execution created")

        else:
            job_service.update_job_execution(
                job_id=job_id,
                execution_id=execution_id,
                status=ExecutionStatus.IN_PROGRESS,
                log_url=None,
                retry_count=receive_count - 1,
                finished_at=None
            )
            execution_logger.log("Execution retry detected")
            
        try:

            job: JobRecord = job_service.get_job(job_id, user_id)
            execution_logger.log("Fetched job metadata")

            execution_logger.log(f"Execution task {job.task_type}")
            email_service.send_email(
                to=job.task_input.to,
                from_email=job.task_input.sender_email,
                subject=job.task_input.subject,
                body=job.task_input.content,
            )

            execution_logger.log("Task executes successfully")
            log_url = log_service.upload_log(
                job_id, execution_id, execution_logger.get_logs()
            )
                
            job_service.update_job_execution(
                job_id=job_id,
                execution_id=execution_id,
                status=ExecutionStatus.SUCCESS,
                log_url=log_url,
                retry_count=None,
                finished_at=datetime.now(timezone.utc).isoformat()
            )
            
        except Exception as e:
            execution_logger.log(f"Job failed: {str(e)}")
            log_url = log_service.upload_log(
                    job_id, execution_id, execution_logger.get_logs()
            )
                
            job_service.update_job_execution(
                job_id=job_id,
                execution_id=execution_id,
                status=ExecutionStatus.FAILED,
                log_url=log_url,
                retry_count=None,
                finished_at=datetime.now(timezone.utc).isoformat()
            )

            raise
                

