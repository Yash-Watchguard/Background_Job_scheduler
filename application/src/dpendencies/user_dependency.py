from repositories.user_repo import UserRepo
import os

from db.connection import get_db,TABLE_NAME
from repositories.user_repo import UserRepo

from fastapi import Depends


from services.user_service import UserService
from mypy_boto3_dynamodb import DynamoDBClient
import os

def get_user_repo(dynamo_client:DynamoDBClient = Depends(get_db))->UserRepo:
    return UserRepo(
        dynamo_db=dynamo_client,
        table_name=TABLE_NAME
    )
    
def get_user_service(user_repo:UserRepo = Depends(get_user_repo))->UserService:
    return UserService(user_repo)




