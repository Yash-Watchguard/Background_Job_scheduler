import pytest
from unittest.mock import MagicMock

from repositories.user_repo import UserRepo
from models.user_model import User
from errors.app_exception import AppException
from errors.error_registry import ErrorCode


@pytest.fixture
def mock_dynamo_db():
    dynamo = MagicMock()

    # Simulate boto3 exception classes
    class ClientError(Exception):
        pass

    class TransactionCanceledException(Exception):
        pass

    dynamo.exceptions.ClientError = ClientError
    dynamo.exceptions.TransactionCanceledException = TransactionCanceledException

    return dynamo


@pytest.fixture
def user_repo(mock_dynamo_db):
    return UserRepo(
        dynamo_db=mock_dynamo_db,
        table_name="user-table"
    )


@pytest.fixture
def user_model():
    return User(
        Name="Test User",
        Id="user-123",
        Email="test@gmail.com",
        Password="hashed-pass",
        PhoneNumber="9999999999"
    )


def test_get_user_by_email_success(user_repo, mock_dynamo_db, user_model):
    mock_dynamo_db.execute_statement.return_value = {
        "Items": [
            {
                "Name": {"S": "Test User"},
                "Id": {"S": "user-123"},
                "Email": {"S": "test@gmail.com"},
                "Password": {"S": "hashed-pass"},
                "PhoneNumber": {"S": "9999999999"},
            }
        ]
    }
    
    from helper.serializer_deserializer import dynamo_to_model
    original = dynamo_to_model

    def fake_serializer(item, model):
        return user_model

    import helper.serializer_deserializer
    helper.serializer_deserializer.dynamo_to_model = fake_serializer

    user = user_repo.get_user_by_email("test@gmail.com")

    assert user.email == "test@gmail.com"
    assert user.id == "user-123"

    helper.serializer_deserializer.dynamo_to_model = original


def test_get_user_by_email_not_found(user_repo, mock_dynamo_db):
    mock_dynamo_db.execute_statement.return_value = {"Items": []}

    with pytest.raises(AppException) as exc:
        user_repo.get_user_by_email("missing@gmail.com")

    assert exc.value.error_code == ErrorCode.USER_NOT_FOUND


def test_get_user_by_email_db_error(user_repo, mock_dynamo_db):
    mock_dynamo_db.execute_statement.side_effect = (
        mock_dynamo_db.exceptions.ClientError("db error")
    )

    with pytest.raises(AppException) as exc:
        user_repo.get_user_by_email("test@gmail.com")

    assert exc.value.error_code == ErrorCode.DB_ERROR



def test_save_user_success(user_repo, mock_dynamo_db, user_model):
    mock_dynamo_db.execute_statement.return_value = None

    user_repo.save_user(user_model)

    mock_dynamo_db.execute_statement.assert_called_once()


def test_save_user_already_present(user_repo, mock_dynamo_db, user_model):
    mock_dynamo_db.execute_statement.side_effect = (
        mock_dynamo_db.exceptions.TransactionCanceledException("duplicate")
    )

    with pytest.raises(AppException) as exc:
        user_repo.save_user(user_model)

    assert exc.value.error_code == ErrorCode.USER_ALREADY_PRESENT


def test_save_user_db_error(user_repo, mock_dynamo_db, user_model):
    mock_dynamo_db.execute_statement.side_effect = (
        mock_dynamo_db.exceptions.ClientError("db error")
    )

    with pytest.raises(AppException) as exc:
        user_repo.save_user(user_model)

    assert exc.value.error_code == ErrorCode.DB_ERROR
