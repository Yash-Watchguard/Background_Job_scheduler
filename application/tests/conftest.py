import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from api.auth_api import auth_router
from dpendencies.auth_dependecy import get_auth_service
from errors.exception_handler import register_exception_handler
from dpendencies.job_dependency import get_job_service
from helper.jwt import varify_jwt
from models.jwt_payload import JwtPayload
from api.job_api import job_router
from services.job_service import JobService

from repositories.user_repo import UserRepo

@pytest.fixture
def mock_job_repo():
    return MagicMock()


@pytest.fixture
def mock_scheduler_service():
    return MagicMock()


@pytest.fixture
def job_service(mock_job_repo, mock_scheduler_service):
    return JobService(mock_job_repo, mock_scheduler_service)


@pytest.fixture
def mock_user_repo():
    return MagicMock(spec=UserRepo)


@pytest.fixture
def mock_auth_service():
  
    return MagicMock()

@pytest.fixture
def mock_job_service():
    return MagicMock()


@pytest.fixture
def mock_jwt_payload():
    return MagicMock()


@pytest.fixture
def test_client(mock_auth_service, mock_job_service,mock_jwt_payload):
    app = FastAPI()

    register_exception_handler(app)

    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    app.dependency_overrides[get_job_service] = lambda: mock_job_service
    app.dependency_overrides[varify_jwt] = lambda: mock_jwt_payload


    app.include_router(auth_router)
    app.include_router(job_router)
    

    return TestClient(app)
