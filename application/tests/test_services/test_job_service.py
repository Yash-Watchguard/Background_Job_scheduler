import pytest
from unittest.mock import MagicMock, patch

from services.job_service import JobService
from errors.app_exception import AppException
from errors.error_registry import ErrorCode
from enums.job_status import JobStatus



@patch("services.job_service.generate_uuid", return_value="job-123")
@patch("services.job_service.validate_schedule")
@patch("services.job_service.get_schedule_expression", return_value="rate(5 minutes)")
def test_create_job_success(
    mock_get_expression,
    mock_validate,
    mock_generate_uuid,
    job_service
):
    job_data = MagicMock()
    job_data.schedule_type = "INTERVAL"
    job_data.job_type = "RECURRING"
    job_data.schedule_time = "*/5 * * * *"

    job_service.create_job(job_data, user_id="user-1")

    mock_validate.assert_called_once_with(
        job_data.schedule_type,
        job_data.job_type
    )

    mock_get_expression.assert_called_once_with(
        job_data.schedule_type,
        job_data.schedule_time
    )

    job_service.scheduler_service.create_new_schedule.assert_called_once()
    job_service.job_repo.put_new_job.assert_called_once()



def test_get_scheduled_job(job_service, mock_job_repo):
    mock_job_repo.get_job.return_value = "job-object"

    result = job_service.get_scheduled_job("user-1", "job-1")

    assert result == "job-object"
    mock_job_repo.get_job.assert_called_once_with("user-1", "job-1")



def test_get_job_executions(job_service, mock_job_repo):
    mock_job_repo.get_job_executions.return_value = ["exec1", "exec2"]

    result = job_service.get_job_executions("job-1")

    assert result == ["exec1", "exec2"]
    mock_job_repo.get_job_executions.assert_called_once_with("job-1")




def test_delete_job_success(job_service, mock_job_repo):
    job = MagicMock()
    job.created_by = "user-1"
    mock_job_repo.get_job.return_value = job

    job_service.delete_job("job-1", "user-1")

    job_service.scheduler_service.delete_scheduler.assert_called_once_with("job-1")
    mock_job_repo.update_job_status.assert_called_once_with(
        "user-1", "job-1", JobStatus.DELETE.value
    )


def test_delete_job_unauthorized(job_service, mock_job_repo):
    job = MagicMock()
    job.created_by = "other-user"
    mock_job_repo.get_job.return_value = job

    with pytest.raises(AppException) as exc:
        job_service.delete_job("job-1", "user-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND


def test_delete_job_not_found(job_service, mock_job_repo):
    mock_job_repo.get_job.side_effect = AppException(
        error_code=ErrorCode.JOB_NOT_FOUND
    )

    with pytest.raises(AppException) as exc:
        job_service.delete_job("job-1", "user-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND



def test_deactivate_job_success(job_service, mock_job_repo):
    job = MagicMock()
    job.created_by = "user-1"
    mock_job_repo.get_job.return_value = job

    job_service.deactivate_job("job-1", "user-1")

    job_service.scheduler_service.deacivate_scheduler.assert_called_once_with("job-1")
    mock_job_repo.update_job_status.assert_called_once_with(
        "user-1", "job-1", JobStatus.IN_ACTIVE.value
    )


def test_deactivate_job_unauthorized(job_service, mock_job_repo):
    job = MagicMock()
    job.created_by = "other-user"
    mock_job_repo.get_job.return_value = job

    with pytest.raises(AppException) as exc:
        job_service.deactivate_job("job-1", "user-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND


def test_deactivate_job_not_found(job_service, mock_job_repo):
    mock_job_repo.get_job.side_effect = AppException(
        error_code=ErrorCode.JOB_NOT_FOUND
    )

    with pytest.raises(AppException) as exc:
        job_service.deactivate_job("job-1", "user-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND



def test_activate_job_success(job_service, mock_job_repo):
    job = MagicMock()
    job.created_by = "user-1"
    mock_job_repo.get_job.return_value = job

    job_service.activate_job("job-1", "user-1")

    job_service.scheduler_service.activate_scheduler.assert_called_once_with("job-1")
    mock_job_repo.update_job_status.assert_called_once_with(
        "user-1", "job-1", JobStatus.ACTIVE.value
    )


def test_activate_job_unauthorized(job_service, mock_job_repo):
    job = MagicMock()
    job.created_by = "other-user"
    mock_job_repo.get_job.return_value = job

    with pytest.raises(AppException) as exc:
        job_service.activate_job("job-1", "user-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND


def test_activate_job_not_found(job_service, mock_job_repo):
    mock_job_repo.get_job.side_effect = AppException(
        error_code=ErrorCode.JOB_NOT_FOUND
    )

    with pytest.raises(AppException) as exc:
        job_service.activate_job("job-1", "user-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND
