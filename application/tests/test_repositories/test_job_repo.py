import pytest
from unittest.mock import MagicMock

from repositories.job_repo import JobRepo
from errors.app_exception import AppException
from errors.error_registry import ErrorCode




@pytest.fixture
def mock_dynamo_db():
    dynamo = MagicMock()

    class ClientError(Exception):
        pass

    dynamo.exceptions.ClientError = ClientError
    return dynamo


@pytest.fixture
def job_repo(mock_dynamo_db):
    return JobRepo(
        dynamo_db=mock_dynamo_db,
        table_name="job-table"
    )


@pytest.fixture
def fake_job_request():
    job_req = MagicMock()
    job_req.job_type.value = "RECURRING"
    job_req.schedule_type.value = "INTERVAL"
    job_req.schedule_time = "*/5 * * * *"
    job_req.task_type.value = "EMAIL"

    task_input = MagicMock()
    task_input.to = ["a@gmail.com", "b@gmail.com"]
    task_input.sender_email = "sender@gmail.com"
    task_input.subject = "test"
    task_input.content = "hello"

    job_req.task_input = task_input
    return job_req



def test_put_new_job_success(job_repo, mock_dynamo_db, fake_job_request):
    mock_dynamo_db.execute_statement.return_value = None

    result = job_repo.put_new_job(
        job_id="job-1",
        user_id="user-1",
        job_request=fake_job_request
    )

    assert result is True
    mock_dynamo_db.execute_statement.assert_called_once()


def test_put_new_job_client_error(job_repo, mock_dynamo_db, fake_job_request):
    mock_dynamo_db.execute_statement.side_effect = (
        mock_dynamo_db.exceptions.ClientError("db error")
    )

    with pytest.raises(AppException) as exc:
        job_repo.put_new_job(
            job_id="job-1",
            user_id="user-1",
            job_request=fake_job_request
        )

    assert exc.value.error_code == ErrorCode.JOB_CREATION_FAILED



from unittest.mock import patch, MagicMock

def test_get_job_success(job_repo, mock_dynamo_db):
    item = {
        "JobId": {"S": "job-1"},
    }

    mock_dynamo_db.execute_statement.return_value = {"Items": [item]}

    fake_job = MagicMock()

    with patch("repositories.job_repo.dynamo_to_model", return_value=fake_job):
        job = job_repo.get_job("user-1", "job-1")

    assert job is fake_job



def test_get_job_not_found(job_repo, mock_dynamo_db):
    mock_dynamo_db.execute_statement.return_value = {"Items": []}

    with pytest.raises(AppException) as exc:
        job_repo.get_job("user-1", "job-1")

    assert exc.value.error_code == ErrorCode.JOB_NOT_FOUND


def test_get_job_db_error(job_repo, mock_dynamo_db):
    mock_dynamo_db.execute_statement.side_effect = (
        mock_dynamo_db.exceptions.ClientError("db error")
    )

    with pytest.raises(AppException) as exc:
        job_repo.get_job("user-1", "job-1")

    assert exc.value.error_code == ErrorCode.DB_ERROR


from unittest.mock import patch, MagicMock

def test_get_job_executions_success(job_repo, mock_dynamo_db):
    items = [
        {"ExecutionId": {"S": "exec-1"}},
        {"ExecutionId": {"S": "exec-2"}},
    ]

    mock_dynamo_db.execute_statement.return_value = {"Items": items}

    fake_execution = MagicMock()

    with patch(
        "repositories.job_repo.dynamo_to_model",
        side_effect=[fake_execution, fake_execution],
    ):
        executions = job_repo.get_job_executions("job-1")

    assert len(executions) == 2



def test_get_job_executions_empty(job_repo, mock_dynamo_db):
    mock_dynamo_db.execute_statement.return_value = {"Items": []}

    result = job_repo.get_job_executions("job-1")

    assert result == []


def test_get_job_executions_db_error(job_repo, mock_dynamo_db):
    mock_dynamo_db.execute_statement.side_effect = (
        mock_dynamo_db.exceptions.ClientError("db error")
    )

    with pytest.raises(AppException) as exc:
        job_repo.get_job_executions("job-1")

    assert exc.value.error_code == ErrorCode.FAILED_TO_FETCH_JOB_EXECUTIONS


def test_update_job_status_success(job_repo, mock_dynamo_db):
    job_repo.update_job_status("user-1", "job-1", "ACTIVE")

    mock_dynamo_db.execute_statement.assert_called_once()


def test_update_job_status_db_error(job_repo, mock_dynamo_db):
    mock_dynamo_db.execute_statement.side_effect = (
        mock_dynamo_db.exceptions.ClientError("db error")
    )

    with pytest.raises(AppException) as exc:
        job_repo.update_job_status("user-1", "job-1", "ACTIVE")

    assert exc.value.error_code == ErrorCode.JOB_UPDATE_FAILED
