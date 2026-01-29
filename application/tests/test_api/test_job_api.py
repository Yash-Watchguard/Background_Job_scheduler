import pytest
from fastapi import status
from unittest.mock import MagicMock
from datetime import datetime

from errors.app_exception import AppException
from errors.error_registry import ErrorCode
from constants.success_message import SuccessMessage


class TestJobAPI:

    def test_create_job_success(self, test_client, mock_job_service):
        mock_job_service.create_job.return_value = None

        payload = {
            "job_type": "RECURRING",
            "schedule_type": "INTERVAL",
            "schedule_time": "*/4 * * * ? *",
            "task_type": "EMPLOYEE_ONE_TIME_NOTIFICATION",
            "task_input": {
                "to": ["test@gmail.com"],
                "sender_email": "sender@gmail.com",
                "subject": "test",
                "content": "hello"
            }
        }

        response = test_client.post("/v1/job", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        body = response.json()

        assert body["status"] == "success"
        assert body["message"] == SuccessMessage.JOB_CREATION

        mock_job_service.create_job.assert_called_once()


    def test_create_job_validation_error(self, test_client):
        response = test_client.post("/v1/job", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

  
    def test_create_job_service_error(self, test_client, mock_job_service):
        mock_job_service.create_job.side_effect = AppException(
            error_code=ErrorCode.JOB_CREATION_FAILED
        )

        payload = {
            "job_type": "RECURRING",
            "schedule_type": "INTERVAL",
            "schedule_time": "*/4 * * * ? *",
            "task_type": "EMPLOYEE_ONE_TIME_NOTIFICATION",
            "task_input": {
                "to": ["test@gmail.com"],
                "sender_email": "sender@gmail.com",
                "subject": "test",
                "content": "hello"
            }
        }

        response = test_client.post("/v1/job", json=payload)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


    def test_get_job_success(self, test_client, mock_job_service):
        mock_job_service.get_scheduled_job.return_value = {
            "job_id": "job-123",
            "status": "ACTIVE"
        }

        response = test_client.get("/v1/job/job-123")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["job_id"] == "job-123"


    def test_get_job_not_found(self, test_client, mock_job_service):
        mock_job_service.get_scheduled_job.side_effect = AppException(
            error_code=ErrorCode.JOB_NOT_FOUND
        )

        response = test_client.get("/v1/job/job-123")

        assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_get_job_executions_success(self, test_client, mock_job_service):
        execution = MagicMock()
        execution.execution_id = "exec-1"
        execution.status.value = "SUCCESS"
        execution.retry_count = 1
        execution.log_url = "http://log"
        execution.started_at = datetime.now()
        execution.finished_at = datetime.now()

        mock_job_service.get_job_executions.return_value = [execution]

        response = test_client.get("/v1/jobs/job-123/executions")

        assert response.status_code == status.HTTP_200_OK
        body = response.json()

        assert body["status"] == "success"
        assert len(body["data"]) == 1
        assert body["data"][0]["execution_id"] == "exec-1"

  
  
    def test_get_job_executions_error(self, test_client, mock_job_service):
        mock_job_service.get_job_executions.side_effect = AppException(
            error_code=ErrorCode.FAILED_TO_FETCH_JOB_EXECUTIONS
        )

        response = test_client.get("/v1/jobs/job-123/executions")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


    def test_delete_job_success(self, test_client, mock_job_service):
        response = test_client.delete("/v1/job/job-123")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "job deleted successfully"



    def test_delete_job_failure(self, test_client, mock_job_service):
        mock_job_service.delete_job.side_effect = AppException(
            error_code=ErrorCode.JOB_DELETION_FAILED
        )

        response = test_client.delete("/v1/job/job-123")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR



    def test_deactivate_job_success(self, test_client):
        response = test_client.patch("/v1/job/job-123/deactivate")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "job terminated successfully"

   
   
    def test_activate_job_success(self, test_client):
        response = test_client.patch("/v1/job/job-123/activate")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "job activates successfully"
