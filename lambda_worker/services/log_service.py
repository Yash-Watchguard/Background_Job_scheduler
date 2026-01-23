from core.aws_clients import s3
from core.config import LOG_BUCKET
class LogService:
    def __init__(self):
        self.s3_client = s3
        
        
    def upload_log(job_id:str, execution_id:str,logs:str):
        key = f"job_id={job_id}/execution_id={execution_id}.log"

        s3.put_object(
            Bucket=LOG_BUCKET,
            Key=key,
            Body=logs.encode("utf-8"),
            ContentType="text/plain",
        )

        return f"s3://{LOG_BUCKET}/{key}"