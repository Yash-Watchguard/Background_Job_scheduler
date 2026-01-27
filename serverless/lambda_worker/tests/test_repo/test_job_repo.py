import pytest
from unittest.mock import patch, MagicMock

from repositories.job_repo import JobRepo
from enums.execution_status import ExecutionStatus
from models.job_execution_model import ExecutionModel


@pytest.fixture
def repo():
    return JobRepo()




@patch("repositories.job_repo.dynamo_to_model")
def test_get_job_success(mock_dynamo_to_model, repo):
    repo.ddb_client = MagicMock()

    fake_item = {"JobId": {"S": "job-1"}}
    fake_job = MagicMock()

    repo.ddb_client.execute_statement.return_value = {"Items": [fake_item]}
    mock_dynamo_to_model.return_value = fake_job

    result = repo.get_job("user-1", "job-1")

    assert result == fake_job
    repo.ddb_client.execute_statement.assert_called_once()
    mock_dynamo_to_model.assert_called_once_with(fake_item, repo.get_job.__annotations__["return"])



def test_get_job_dynamodb_error(repo):
    class ClientError(Exception):
        pass

    repo.ddb_client = MagicMock()
    repo.ddb_client.exceptions = MagicMock()
    repo.ddb_client.exceptions.ClientError = ClientError
    repo.ddb_client.execute_statement.side_effect = ClientError("boom")

    with pytest.raises(Exception, match="DynamoDB error in get_job"):
        repo.get_job("user-1", "job-1")




def test_post_job_execution_success(repo):
    repo.ddb_client = MagicMock()

    execution = MagicMock()
    execution.execution_id = "exec-1"
    execution.job_id = "job-1"
    execution.status.value = ExecutionStatus.STARTED.value
    execution.log_url = None
    execution.started_at.isoformat.return_value = "now"
    execution.finished_at = None
    execution.retry_count = 0
    execution.max_retries = 3

    assert repo.post_job_execution("job-1", execution) is True
    repo.ddb_client.execute_statement.assert_called_once()


def test_post_job_execution_dynamodb_error(repo):
    class ClientError(Exception):
        pass

    repo.ddb_client = MagicMock()
    repo.ddb_client.exceptions = MagicMock()
    repo.ddb_client.exceptions.ClientError = ClientError
    repo.ddb_client.execute_statement.side_effect = ClientError("boom")

    execution = MagicMock()
    execution.execution_id = "exec-1"
    execution.job_id = "job-1"
    execution.status.value = ExecutionStatus.STARTED.value
    execution.log_url = None
    execution.started_at.isoformat.return_value = "now"
    execution.finished_at = None
    execution.retry_count = 0
    execution.max_retries = 3

    with pytest.raises(Exception, match="DynamoDB error in post_job_execution"):
        repo.post_job_execution("job-1", execution)




def test_update_job_execution_all_fields(repo):
    repo.ddb_client = MagicMock()

    assert repo.update_job_execution(
        job_id="job-1",
        execution_id="exec-1",
        status=ExecutionStatus.SUCCESS,
        retry_count=1,
        finished_at="done",
        log_url="s3://log",
    ) is True

    repo.ddb_client.execute_statement.assert_called_once()


def test_update_job_execution_min_fields(repo):
    repo.ddb_client = MagicMock()

    assert repo.update_job_execution(
        job_id="job-1",
        execution_id="exec-1",
        status=ExecutionStatus.FAILED,
    ) is True

    repo.ddb_client.execute_statement.assert_called_once()


def test_update_job_execution_dynamodb_error(repo):
    class ClientError(Exception):
        pass

    repo.ddb_client = MagicMock()
    repo.ddb_client.exceptions = MagicMock()
    repo.ddb_client.exceptions.ClientError = ClientError
    repo.ddb_client.execute_statement.side_effect = ClientError("boom")

    with pytest.raises(Exception, match="DynamoDB error in update_job_execution"):
        repo.update_job_execution(
            job_id="job-1",
            execution_id="exec-1",
            status=ExecutionStatus.FAILED,
        )


@patch("repositories.job_repo.dynamo_to_model")
def test_get_job_execution_success(mock_dynamo_to_model, repo):
    repo.ddb_client = MagicMock()

    fake_item = {"ExecutionId": {"S": "exec-1"}}
    fake_execution = MagicMock()

    repo.ddb_client.execute_statement.return_value = {"Items": [fake_item]}
    mock_dynamo_to_model.return_value = fake_execution

    result = repo.get_job_execution("job-1", "exec-1")

    assert result == fake_execution
    mock_dynamo_to_model.assert_called_once_with(fake_item, ExecutionModel)


def test_get_job_execution_not_found(repo):
    repo.ddb_client = MagicMock()
    repo.ddb_client.execute_statement.return_value = {"Items": []}

    assert repo.get_job_execution("job-1", "exec-1") is None


def test_get_job_execution_dynamodb_error(repo):
    class ClientError(Exception):
        pass

    repo.ddb_client = MagicMock()
    repo.ddb_client.exceptions = MagicMock()
    repo.ddb_client.exceptions.ClientError = ClientError
    repo.ddb_client.execute_statement.side_effect = ClientError("boom")

    with pytest.raises(Exception, match="DynamoDB error in get_EXECUTION"):
        repo.get_job_execution("job-1", "exec-1")
