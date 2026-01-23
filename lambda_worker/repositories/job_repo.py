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
                raise Exception("error occured")

            return dynamo_to_model(items[0], JobRecord)

        except self.ddb_client.exceptions.ClientError as e:
            raise Exception("error occured")
        
    
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
        }}
        """

        parameters = [
            {"S": f"JOB#{job_id}"},
            {"S": f"EXECUTION#{execution_model.Execution_id}"},
            {"S": execution_model.Execution_id},
            {"S": execution_model.job_id},
            {"S": execution_model.status.value},
            (
                {"S": execution_model.log_url}
                if execution_model.log_url
                else {"NULL": True}
            ),

        ]

        try:
            self.ddb_client.execute_statement(
                Statement=statement,
                Parameters=parameters
            )
        except self.ddb_client.exceptions.ClientError as e:
            raise Exception

        return True
    
    def update_job_execution(
        self,
        job_id: str,
        execution_id: str,
        status: ExecutionStatus,
        log_url: str | None = None,
    ) -> bool:
       
        statement = f"""
        UPDATE "{self.table_name}"
        SET
            #s = ?,
            LogUrl = ?
        WHERE
            pk = ? AND sk = ?
        """

        parameters = [
            {"S": status.value},
            (
                {"S": log_url}
                if log_url
                else {"NULL": True}
            ),
            {"S": f"JOB#{job_id}"},
            {"S": f"EXECUTION#{execution_id}"},
        ]

        try:
            self.ddb_client.execute_statement(
                Statement=statement,
                Parameters=parameters,
                ExpressionAttributeNames={
                    "#s": "Status"
                }
            )

        except self.ddb_client.exceptions.ClientError as e:
            raise Exception from e

        return True
        