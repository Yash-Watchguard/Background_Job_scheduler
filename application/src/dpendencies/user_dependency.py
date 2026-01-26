from repositories.user_repo import UserRepo
import os

from core.aws_clients import get_db
from core.config import TABLE_NAME
from repositories.user_repo import UserRepo

from fastapi import Depends



from mypy_boto3_dynamodb import DynamoDBClient
import os

def get_user_repo(dynamo_client:DynamoDBClient = Depends(get_db))->UserRepo:
    return UserRepo(
        dynamo_db=dynamo_client,
        table_name=TABLE_NAME
    )
    




