import json
import pytest
from unittest.mock import MagicMock

from services.scheduler_service import SchedulerService
from errors.app_exception import AppException
from errors.error_registry import ErrorCode




@pytest.fixture
def mock_scheduler_client():
    client = MagicMock()

    class ResourceNotFoundException(Exception):
        pass

    client.exceptions.ResourceNotFoundException = ResourceNotFoundException
    return client


@pytest.fixture
def scheduler_service(mock_scheduler_client):
    return SchedulerService(
        scheduler_client=mock_scheduler_client,
        event_bridge_role_arn="arn:aws:iam::123:role/test",
        schedule_group_name="test-group"
    )


def test_create_new_schedule_success(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.create_schedule.return_value = {"status": "ok"}

    response = scheduler_service.create_new_schedule(
        job_id="job-1",
        user_id="user-1",
        target_queue_arn="arn:aws:sqs:test",
        schedule_expression="cron(5 minutes)"
    )

    assert response == {"status": "ok"}
    mock_scheduler_client.create_schedule.assert_called_once()

    
    args, kwargs = mock_scheduler_client.create_schedule.call_args
    payload = json.loads(kwargs["Target"]["Input"])
    assert payload["job_id"] == "job-1"
    assert payload["user_id"] == "user-1"


def test_create_new_schedule_failure(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.create_schedule.side_effect = Exception("aws error")

    with pytest.raises(AppException) as exc:
        scheduler_service.create_new_schedule(
            "job-1", "user-1", "arn:queue", "rate(5 minutes)"
        )

    assert exc.value.error_code == ErrorCode.JOB_CREATION_FAILED



def test_delete_scheduler_success(scheduler_service, mock_scheduler_client):
    scheduler_service.delete_scheduler("job-1")
    mock_scheduler_client.delete_schedule.assert_called_once()


def test_delete_scheduler_not_found(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.delete_schedule.side_effect = (
        mock_scheduler_client.exceptions.ResourceNotFoundException("not found")
    )

    with pytest.raises(AppException) as exc:
        scheduler_service.delete_scheduler("job-1")

    assert exc.value.error_code == ErrorCode.SCHEDULE_NOT_FOUND


def test_delete_scheduler_generic_error(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.delete_schedule.side_effect = Exception("aws error")

    with pytest.raises(AppException) as exc:
        scheduler_service.delete_scheduler("job-1")

    assert exc.value.error_code == ErrorCode.JOB_DELETION_FAILED


def test_get_scheduler_details_success(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.get_schedule.return_value = {
        "ScheduleExpression": "rate(5 minutes)",
        "Target": {"Arn": "arn:queue"}
    }

    result = scheduler_service.get_scheduler_details("job-1")

    assert result["schedule_expression"] == "rate(5 minutes)"
    assert result["target"]["Arn"] == "arn:queue"


def test_get_scheduler_details_not_found(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.get_schedule.side_effect = (
        mock_scheduler_client.exceptions.ResourceNotFoundException("not found")
    )

    with pytest.raises(AppException) as exc:
        scheduler_service.get_scheduler_details("job-1")

    assert exc.value.error_code == ErrorCode.SCHEDULE_NOT_FOUND


def test_get_scheduler_details_generic_error(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.get_schedule.side_effect = Exception("aws error")

    with pytest.raises(AppException) as exc:
        scheduler_service.get_scheduler_details("job-1")

    assert exc.value.error_code == ErrorCode.INTERNAL_SERVER_ERROR



def test_deactivate_scheduler_success(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.get_schedule.return_value = {
        "ScheduleExpression": "rate(5 minutes)",
        "Target": {"Arn": "arn:queue"}
    }

    scheduler_service.deacivate_scheduler("job-1")

    mock_scheduler_client.update_schedule.assert_called_once()
    assert mock_scheduler_client.update_schedule.call_args.kwargs["State"] == "DISABLED"


def test_deactivate_scheduler_not_found(scheduler_service, mock_scheduler_client):
    scheduler_service.get_scheduler_details = MagicMock(
        side_effect=mock_scheduler_client.exceptions.ResourceNotFoundException("nf")
    )

    with pytest.raises(AppException) as exc:
        scheduler_service.deacivate_scheduler("job-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND


def test_deactivate_scheduler_generic_error(scheduler_service, mock_scheduler_client):
    scheduler_service.get_scheduler_details = MagicMock(
        side_effect=Exception("aws error")
    )

    with pytest.raises(AppException) as exc:
        scheduler_service.deacivate_scheduler("job-1")

    assert exc.value.error_code == ErrorCode.INTERNAL_SERVER_ERROR



def test_activate_scheduler_success(scheduler_service, mock_scheduler_client):
    mock_scheduler_client.get_schedule.return_value = {
        "ScheduleExpression": "rate(5 minutes)",
        "Target": {"Arn": "arn:queue"}
    }

    scheduler_service.activate_scheduler("job-1")

    mock_scheduler_client.update_schedule.assert_called_once()
    assert mock_scheduler_client.update_schedule.call_args.kwargs["State"] == "ENABLED"


def test_activate_scheduler_not_found(scheduler_service, mock_scheduler_client):
    scheduler_service.get_scheduler_details = MagicMock(
        side_effect=mock_scheduler_client.exceptions.ResourceNotFoundException("nf")
    )

    with pytest.raises(AppException) as exc:
        scheduler_service.activate_scheduler("job-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND


def test_activate_scheduler_generic_error(scheduler_service, mock_scheduler_client):
    scheduler_service.get_scheduler_details = MagicMock(
        side_effect=Exception("aws error")
    )

    with pytest.raises(AppException) as exc:
        scheduler_service.activate_scheduler("job-1")

    assert exc.value.error_code == ErrorCode.INTERNAL_SERVER_ERROR
