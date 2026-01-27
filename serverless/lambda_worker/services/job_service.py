from repositories.job_repo import JobRepo
from models.job_model import JobRecord
from models.job_execution_model import ExecutionModel
from enums.execution_status import ExecutionStatus
from datetime import datetime, timezone
from uuid import uuid4


class JobService:
    def __init__(self, job_repo: JobRepo):
        self.job_repo = job_repo

    def get_job(self, job_id: str, user_id: str) -> JobRecord:
        return self.job_repo.get_job(user_id, job_id)

    def post_job_execution(self, job_id: str, execution_id: str) -> str:
        execution_model = ExecutionModel(
            ExecutionId=execution_id,
            JobId=job_id,
            StartedAt=datetime.now(timezone.utc),
            MaxRetries=3,
            Status=ExecutionStatus.STARTED,
        )
        self.job_repo.post_job_execution(job_id, execution_model)
        return execution_model.execution_id

    def update_job_execution(
        self,
        job_id: str,
        execution_id: str,
        status: ExecutionStatus,
        log_url: str | None = None,
        retry_count: int | None = None,
        finished_at: str | None = None,
    ):
        return self.job_repo.update_job_execution(
            job_id, execution_id, status, retry_count, finished_at, log_url
        )

    def get_job_execution(self, job_id: str, execution_id: str):
        return self.job_repo.get_job_execution(job_id, execution_id)
