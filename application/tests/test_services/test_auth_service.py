import pytest
from unittest.mock import patch

from services.auth_service import AuthService
from models.user_model import User
from schemas.user import SignupRequest
from errors.app_exception import AppException
from errors.error_registry import ErrorCode




@patch("services.auth_service.create_jwt_token", return_value="fake-jwt")
@patch("services.auth_service.check_password", return_value=True)
def test_login_success(
    mock_check_password,
    mock_create_jwt,
    mock_user_repo
):
    user = User(
        Name="Test User",
        Id="user-123",
        Email="test@gmail.com",
        Password="hashed-pass",
        PhoneNumber="9999999999"
    )

    mock_user_repo.get_user_by_email.return_value = user

    service = AuthService(mock_user_repo)

    result = service.login("test@gmail.com", "password")

    assert result["UserId"] == "user-123"
    assert result["token"] == "fake-jwt"

    mock_user_repo.get_user_by_email.assert_called_once_with(email="test@gmail.com")
    mock_check_password.assert_called_once()
    mock_create_jwt.assert_called_once_with("user-123")


@patch("services.auth_service.check_password", return_value=False)
def test_login_invalid_password(
    mock_check_password,
    mock_user_repo
):
    user = User(
        Name="Test User",
        Id="user-123",
        Email="test@gmail.com",
        Password="hashed-pass",
        PhoneNumber="9999999999"
    )

    mock_user_repo.get_user_by_email.return_value = user

    service = AuthService(mock_user_repo)

    with pytest.raises(AppException) as exc:
        service.login("test@gmail.com", "wrong")

    assert exc.value.error_code == ErrorCode.INVALID_CREDENTIAL




def test_signup_user_already_exists(mock_user_repo):
    mock_user_repo.get_user_by_email.return_value = User(
        Name="Existing User",
        Id="existing-id",
        Email="test@gmail.com",
        Password="hashed-pass",
        PhoneNumber="9999999999"
    )

    service = AuthService(mock_user_repo)

    req = SignupRequest(
        email="test@gmail.com",
        name="Test",
        password="Password@123",
        phone_number="9999999999"
    )

    with pytest.raises(AppException) as exc:
        service.signup(req)

    assert exc.value.error_code == ErrorCode.USER_ALREADY_PRESENT


@patch("services.auth_service.generate_hash_password", return_value="hashed-password")
@patch("services.auth_service.generate_uuid", return_value="uuid-123")
def test_signup_success(
    mock_generate_uuid,
    mock_generate_hash,
    mock_user_repo
):
    mock_user_repo.get_user_by_email.return_value = None

    service = AuthService(mock_user_repo)

    req = SignupRequest(
        name="yash",
        email="yashgoyal@gmal.com",
        password="Yashgoyal@#123",
        phonenumber="7737063944"
    )

    user:User = service.signup(req)

    assert user.id == "uuid-123"
    assert user.email == "yashgoyal@gmal.com"
    assert user.phone_number == "7737063944"

    mock_generate_uuid.assert_called_once()
    mock_generate_hash.assert_called_once_with("Yashgoyal@#123")
    mock_user_repo.save_user.assert_called_once()
