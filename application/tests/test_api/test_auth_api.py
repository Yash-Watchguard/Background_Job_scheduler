import pytest
from fastapi import status
from unittest.mock import MagicMock

from errors.app_exception import AppException
from errors.error_registry import ErrorCode
from constants.success_message import SuccessMessage


class TestAuthAPI:

    def test_login_success(self, test_client, mock_auth_service):
        mock_auth_service.login.return_value = {
            "access_token": "fake-token",
            "token_type": "bearer",
        }

        response = test_client.post(
            "/v1/auth/login",
            json={"email": "user@gmail.com", "password": "Password@123"},
        )

        assert response.status_code == status.HTTP_201_CREATED

        body = response.json()
        assert body["status"] == "success"
        assert body["message"] == SuccessMessage.LOGIN
        assert body["data"]["access_token"] == "fake-token"

        mock_auth_service.login.assert_called_once_with(
            "user@gmail.com", "Password@123"
        )

    def test_login_user_not_found(self, test_client, mock_auth_service):
        mock_auth_service.login.side_effect = AppException(
            error_code=ErrorCode.USER_NOT_FOUND
        )

        response = test_client.post(
            "/v1/auth/login", json={"email": "wrong@gmail.com", "password": "123"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

        body = response.json()
        assert body["status"] == "fail"
        assert body["message"] == "User Not Found"
        assert body["errorcode "] == ErrorCode.USER_NOT_FOUND

    def test_login_invalid_password(self, test_client, mock_auth_service):
        mock_auth_service.login.side_effect = AppException(
            error_code=ErrorCode.INVALID_CREDENTIAL
        )

        response = test_client.post(
            "/v1/auth/login", json={"email": "user@gmail.com", "password": "wrong"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        body = response.json()
        assert body["message"] == "Invalid Password , please check"

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"email": "user@gmail.com"},
            {"password": "123"},
            {"email": "invalid", "password": "123"},
        ],
    )
    def test_login_validation_error(self, test_client, payload):
        response = test_client.post("/v1/auth/login", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        body = response.json()
        assert body["status"] == "fail"
        assert body["errorcode "] == ErrorCode.VALIDATION_ERROR

    def test_signup_success(self, test_client, mock_auth_service):
        mock_auth_service.signup.return_value = {"id": "123", "email": "user@gmail.com"}

        response = test_client.post(
            "/v1/auth/signup",
            json={
                "name": "yash",
                "email": "yashgoyal322023@gmail.com",
                "password": "Yashgoyal@#123",
                "phonenumber": "8619864794",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

        body = response.json()
        assert body["status"] == "success"
        assert body["message"] == SuccessMessage.SIGNUP
        assert body["data"]["email"] == "user@gmail.com"


    def test_signup_user_already_present(self, test_client, mock_auth_service):
        mock_auth_service.signup.side_effect = AppException(
            error_code=ErrorCode.USER_ALREADY_PRESENT
        )

        response = test_client.post(
            "/v1/auth/signup",
            json={
                "name": "yash",
                "email": "yashgoyal322023@gmail.com",
                "password": "Yashgoyal@#123",
                "phonenumber": "8619864794",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT

        body = response.json()
        assert body["message"].startswith("User Is Already Available")

    
    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"email": "user@gmail.com"},
            {"password": "123"},
            {"name": "Yash"},
        ],
    )
    def test_signup_validation_error(self, test_client, payload):
        response = test_client.post("/v1/auth/signup", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
