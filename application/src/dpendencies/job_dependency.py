from db.connection  import get_db, TABLE_NAME
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_s3 import S3Client
from fastapi import Depends
from repositories.job_repo import JobRepo

from core.aws_clients import  eventbridge_scheduler_client
from services.job_service import JobService
from core.config import SCHEDULE_GROUP_NAME, SCHEDULER_ROLE_ARN
from services.scheduler_service import SchedulerService


def get_job_repo(dynamo_client:DynamoDBClient = Depends(get_db))->JobRepo:
    return JobRepo(
        dynamo_db=dynamo_client,
        table_name=TABLE_NAME
    )
    
# def get_s3_service(bucket_name:str = scripts_bucket_name, s3_client = Depends(get_s3_client))->S3Service:
#     return S3Service(
#         s3_client,bucket_name
#     )
    
def get_scheduler_service(role_arn= SCHEDULER_ROLE_ARN,group_name= SCHEDULE_GROUP_NAME, scheduler_client = Depends(eventbridge_scheduler_client))->SchedulerService:
    return SchedulerService(
        scheduler_client,role_arn,group_name
    )
    
def get_job_service( job_repo:JobRepo = Depends(get_job_repo), scheduler_service:SchedulerService = Depends(get_scheduler_service))->JobService:
    return JobService(
        job_repo,scheduler_service
    )