
from fastapi import status

from mypy_boto3_dynamodb import DynamoDBClient

from errors.app_exception import AppException
from constants.custom_error_code_registry import (
    Db_Error,
)
from constants import error_messages
from helper.serializer_deserializer import dynamo_to_model
from schemas.job import JobReqest
from datetime import datetime


class JobRepo:
    def __init__(
        self,
        dynamo_db:DynamoDBClient,
        table_name: str,
    ):
        self.table_name = table_name
        self.dynamo_db = dynamo_db
        
    
    def put_new_job(
        self,
        job_id: str,
        user_id: str,
        job_request: JobReqest,
    ):
        """
        Insert new job using DynamoDB PartiQL
        """

        statement = f"""
        INSERT INTO "{self.table_name}" VALUE {{
            'pk': ?,
            'sk': ?,
            'JobId': ?,
            'JobType': ?,
            'ScheduleType': ?,
            'ScheduleValue': ?,
            'TaskType': ?,
            'TaskInput':?,
            'CreatedAt': ?
        }}
        """

        parameters = [
            {"S":f"USER#{user_id}"},
            {"S" : f"JOBS#{job_id}"},
            {"S": job_id},
            {"S": job_request.job_type.value},
            {"S": job_request.schedule_type.value},
            {"S": job_request.schedule_value},
            {"S": job_request.task_type.value},
            {
                "M": {
                    "To": {"L": [{"S": email} for email in job_request.task_input.to]},
                    "SenderEmail" :{"S": job_request.task_input.sender_email},
                    "Subject": {"S": job_request.task_input.subject},
                    "Content": {"S": job_request.task_input.content},
                }
            },
            {"S": datetime.now().isoformat()},
        ]

        try:
            self.dynamo_db.execute_statement(
                Statement=statement,
                Parameters=parameters
            )

        except self.dynamo_db.exceptions.ClientError as e:
            raise AppException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=Db_Error,
                message=f"error from the db to store the url{str(e)}"
            )


        return True