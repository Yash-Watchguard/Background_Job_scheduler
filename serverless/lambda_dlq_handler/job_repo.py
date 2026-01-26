from core.config import JOB_TABLE
from datetime import datetime, timezone
from enums.execution_status import ExecutionStatus

class JobRepo:
    def __init__(self , dynamo_client):
        self.dynamo_client = dynamo_client
        
    def update_job_execution(self , job_id:str , execution_id:str):
        statement = f"""
            UPDATE "{JOB_TABLE}"
            SET
                Status = ?,
                FinishedAt = ?
            WHERE
                pk = ? AND sk = ?
        """

        parameters = [
            {"S": ExecutionStatus.PERMANENTLY_FAILED.value},
            {"S": datetime.now(timezone.utc).isoformat()},
            {"S": f"JOB#{job_id}"},
            {"S": f"EXECUTION#{execution_id}"},
        ]
        try:
            self.dynamo_client.execute_statement(
                Statement=statement,
                Parameters=parameters,
                ConditionExpression="attribute_exists(pk) AND attribute_exists(sk)"
            )

        except Exception as e:
            raise Exception("error from the dynamodb")
        
        return True
            