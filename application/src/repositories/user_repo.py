from models.user_model import User
from fastapi import status
import asyncio
from mypy_boto3_dynamodb import DynamoDBClient

from errors.app_exception import AppException
from constants.custom_error_code_registry import (
    Db_Error,
    Conflict_Error,
    Unexpected_Error,
)
from constants import error_messages
from helper.serializer_deserializer import dynamo_to_model


class UserRepo:
    def __init__(
        self,
        dynamo_db:DynamoDBClient,
        table_name: str,
    ):
        self.table_name = table_name
        self.dynamo_db = dynamo_db

    def get_user_by_email(self, email: str) -> User:
        statement: str = f'''SELECT * FROM "{self.table_name}" WHERE pk = ? AND sk = ? '''

        try:
            response = self.dynamo_db.execute_statement(
                Statement=statement, Parameters=[{"S": "USER"}, {"S": f"USER#{email}"}]
            )

        except Exception as e:
            print(str(e))
            raise AppException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Eroro in getting the user {str(e)}",
                error_code=Db_Error,
            ) from e

        items = response.get("Items", [])

        if len(items) == 0:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No user present",
                error_code="USER_NOT_FOUND",
            )
        print(items)
        users:list[User] = [dynamo_to_model(item, User) for item in items]
        print(users)
        return users[0]

    def save_user(self, user: User):
        statement = f"""INSERT INTO "{self.table_name}" VALUE {{'pk' : ? , 'sk': ? , 'Name':?, 'Id': ? , 'Email':?, 'Password' :?,'PhoneNumber':? }}"""
        try:
            self.dynamo_db.execute_statement(
                Statement=statement,
                Parameters=[
                    {"S": "USER"},
                    {"S": f"USER#{user.email}"},
                    {"S": f"{user.name}"},
                    {"S": f"{user.id}"},
                    {"S": f"{user.email}"},
                    {"S": f"{user.password}"},
                    {"S": f"{user.phone_number}"}
                ],
            )
            
            print("success")

        except self.dynamo_db.exceptions.TransactionCanceledException as e:

            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                message="User creation failed due to the Conflict ",
                error_code=Conflict_Error,
            )

        except Exception as exception:
            raise AppException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Unexpected error{str(exception)}",
                error_code=Unexpected_Error,
            )
