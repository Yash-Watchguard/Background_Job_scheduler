from models.user_model import User
from errors.app_exception import AppException
from errors.error_registry import ErrorCode
from helper.serializer_deserializer import dynamo_to_model


class UserRepo:
    def __init__(
        self,
        dynamo_db,
        table_name: str,
    ):
        self.table_name = table_name
        self.dynamo_db = dynamo_db

    def get_user_by_email(self, email: str) -> User:
        statement: str = (
            f"""SELECT * FROM "{self.table_name}" WHERE pk = ? AND sk = ? """
        )

        try:
            response = self.dynamo_db.execute_statement(
                Statement=statement, Parameters=[{"S": "USER"}, {"S": f"USER#{email}"}]
            )
            items = response.get("Items", [])

            if len(items) == 0:
                raise AppException(
                    error_code=ErrorCode.USER_NOT_FOUND
                )
            users: list[User] = [dynamo_to_model(item, User) for item in items]
            return users[0]

        except self.dynamo_db.exceptions.ClientError as exception:
            raise AppException(
                error_code=ErrorCode.DB_ERROR,
                detail=exception
            ) from exception


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
                    {"S": f"{user.phone_number}"},
                ],
            )


        except self.dynamo_db.exceptions.TransactionCanceledException as exception:

            raise AppException(
                error_code=ErrorCode.USER_ALREADY_PRESENT,
                detail=str(exception)
            ) from exception

        except self.dynamo_db.exceptions.ClientError as exception:
            raise AppException(
                error_code=ErrorCode.DB_ERROR,
                detail=str(exception)
            ) from exception
