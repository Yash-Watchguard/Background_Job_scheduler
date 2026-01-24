from core.aws_clients import dynamodb
from core.config import JOB_TABLE
from models.job_model import JobRecord
from helper.serializer_deserializer import dynamo_to_model
from models.job_execution_model import ExecutionModel
from enums.execution_status import ExecutionStatus

class JobRepo:
    def __init__(self):
        self.ddb_client =dynamodb
        self.table_name =  JOB_TABLE
        
    def get_job(self, user_id: str, job_id: str) -> JobRecord:
        """
        Fetch job using pk + sk via PartiQL
        """

        statement = f'''
        SELECT *
        FROM "{self.table_name}"
        WHERE pk = ? AND sk = ?
        '''

        parameters = [
            {"S": f"USER#{user_id}"},
            {"S": f"JOBS#{job_id}"},
        ]

        try:
            response = self.ddb_client.execute_statement(
                Statement=statement,
                Parameters=parameters
            )

            items = response.get("Items", [])

            if not items:
                raise Exception("Job not found")

            return dynamo_to_model(items[0], JobRecord)

        except self.ddb_client.exceptions.ClientError as e:
            raise Exception(f"DynamoDB error in get_job: {str(e)}")
        
    
    def post_job_execution(
        self,
        job_id: str,
        execution_model: ExecutionModel
    ) -> bool:
        """
        Insert a new job execution record using DynamoDB PartiQL
        """

        statement = f"""
        INSERT INTO "{self.table_name}" VALUE {{
            'pk': ?,
            'sk': ?,
            'ExecutionId': ?,
            'JobId': ?,
            'Status': ?,
            'LogUrl': ?,
            'StartedAt' :?,
            'FinishedAt': ?,
            'RetryCount':?,
            'MaxRetries':?
        }}
        """

        parameters = [
            {"S": f"JOB#{job_id}"},
            {"S": f"EXECUTION#{execution_model.execution_id}"},
            {"S": execution_model.execution_id},
            {"S": execution_model.job_id},
            {"S": execution_model.status.value},
            (
                {"S": execution_model.log_url}
                if execution_model.log_url
                else {"NULL": True}
            ),
            {"S": execution_model.started_at.isoformat()},
            (
                {"S": execution_model.finished_at.isoformat()}
                if execution_model.finished_at
                else {"NULL": True}
            ),
            {"N": str(execution_model.retry_count)},
            {"N": str(execution_model.max_retries)}
        ]

        try:
            self.ddb_client.execute_statement(
                Statement=statement,
                Parameters=parameters
            )
        except self.ddb_client.exceptions.ClientError as e:
            raise Exception(f"DynamoDB error in post_job_execution: {str(e)}")

        return True
    
    def update_job_execution(
        self,
        job_id: str,
        execution_id: str,
        status: ExecutionStatus,
        retry_count:int|None=None,
        finished_at:str|None = None,
        log_url: str | None = None,
    ) -> bool:
        
        
        set_clauses = ["Status = ?"]
        parameters = [{"S": status.value}]

        if retry_count is not None:
            set_clauses.append("RetryCount = ?")
            parameters.append({"N": str(retry_count)})

        if finished_at is not None:
            set_clauses.append("FinishedAt = ?")
            parameters.append({"S": finished_at})

        if log_url is not None:
            set_clauses.append("LogUrl = ?")
            parameters.append({"S": log_url})

        set_expression = ", ".join(set_clauses)
       
        statement = f"""
            UPDATE "{self.table_name}"
            SET {set_expression}
            WHERE pk = ? AND sk = ?
        """
        
        parameters.extend([
            {"S": f"JOB#{job_id}"},
            {"S": f"EXECUTION#{execution_id}"},
        ])

        try:
            self.ddb_client.execute_statement(
                Statement=statement,
                Parameters=parameters,
            )

        except self.ddb_client.exceptions.ClientError as e:
            raise Exception(f"DynamoDB error in update_job_execution: {str(e)}")

        return True
    
    def get_job_execution(self,job_id:str,execution_id:str):
        
        statement = f'''
        SELECT *
        FROM "{self.table_name}"
        WHERE pk = ? AND sk = ?
        '''

        parameters = [
            {"S": f"JOB#{job_id}"},
            {"S": f"EXECUTION#{execution_id}"},
        ]

        try:
            response = self.ddb_client.execute_statement(
                Statement=statement,
                Parameters=parameters
            )

            items = response.get("Items", [])

            if not items:
                return None

            return dynamo_to_model(items[0], ExecutionModel)

        except self.ddb_client.exceptions.ClientError as e:
            raise Exception(f"DynamoDB error in get_EXECUTION: {str(e)}")