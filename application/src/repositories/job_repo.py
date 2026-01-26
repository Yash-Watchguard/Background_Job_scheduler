
from fastapi import status

from mypy_boto3_dynamodb import DynamoDBClient

from errors.app_exception import AppException


from models.job_execution_model import ExecutionModel
from typing import List

from helper.serializer_deserializer import dynamo_to_model
from schemas.job import JobReqest
from datetime import datetime
from enums.job_status import JobStatus
from models.job_model import JobRecord
from helper.serializer_deserializer import dynamo_to_model
from errors.error_registry import ErrorCode


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
            'CreatedAt': ?,
            'Status' :?,
            'CreatedBy':?
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
            {"S": JobStatus.ACTIVE.value},
            {"S": user_id}
        ]

        try:
            self.dynamo_db.execute_statement(
                Statement=statement,
                Parameters=parameters
            )

        except self.dynamo_db.exceptions.ClientError as exception:
            raise AppException(
                error_code=ErrorCode.JOB_CREATION_FAILED,
                detail=str(exception)
            ) from exception


        return True
    
    def get_job(self, user_id:str ,job_id:str)->JobRecord:
        statement =  f'''
            SELECT * FROM "{self.table_name}" WHERE pk = ? AND sk = ?
        '''
        try:
            response = self.dynamo_db.execute_statement(
                Statement=statement,
                Parameters=[
                    {"S":f"USER#{user_id}"},
                    {"S": f"JOBS#{job_id}"}
                ]
            )
            
            items = response["Items"]
            
            if not items :
                raise AppException(error_code=ErrorCode.JOB_NOT_FOUND)
            
            job:JobRecord = dynamo_to_model(items[0],JobRecord)
            
            return job
            
        except self.dynamo_db.exceptions.ClientError as exception :
            raise AppException(error_code=ErrorCode.DB_ERROR, detail=str(exception)) from exception
            
            
    def get_job_executions(self,job_id:str) -> List[ExecutionModel]:
        statement = f'''
        SELECT * FROM "{self.table_name}" WHERE pk = ? AND begins_with(sk , ?)
        
        '''
        
        try:
            response = self.dynamo_db.execute_statement(
                Statement=statement,
                Parameters=[
                    {"S" : f"JOB#{job_id}"},
                    {"S" :"EXECUTION#"}
                ]
            )
            
            items = response["Items"]

            if not items:
                return []
            
            executions = [dynamo_to_model(item, ExecutionModel) for item in items]
            
            return executions
        
        except self.dynamo_db.exceptions.ClientError as exception:
            raise AppException(
                error_code=ErrorCode.FAILED_TO_FETCH_JOB_EXECUTIONS,
                detail=str(exception)
            ) from exception
            
            
    def update_job_status(self, user_id:str , job_id :str , job_status:str):
        statement = f'''
         UPDATE "{self.table_name}" SET Status = ? WHERE pk = ? AND sk = ?
        '''
        try:
            self.dynamo_db.execute_statement(
                Statement=statement,
                Parameters=[
                    {"S" :job_status},
                    {"S" :f"USER#{user_id}"},
                    {"S": f"JOBS#{job_id}"}
                ],
            )
            
        except self.dynamo_db.exceptions.ClientError as exception:
            raise AppException(error_code=ErrorCode.JOB_UPDATE_FAILED, detail=str(exception)) from exception
            
            

        