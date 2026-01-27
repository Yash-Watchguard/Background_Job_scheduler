
from unittest.mock import MagicMock, ANY
import pytest
from services.job_service import JobService


from enums.execution_status import ExecutionStatus
from models.job_execution_model import ExecutionModel

@pytest.fixture
def mock_job_repo():
    return MagicMock()


@pytest.fixture
def job_service(mock_job_repo):
    return JobService(job_repo=mock_job_repo)

def test_get_job_calls_repo(job_service, mock_job_repo):
    mock_job_repo.get_job.return_value = MagicMock()

    result = job_service.get_job("job-1", "user-1")

    mock_job_repo.get_job.assert_called_once_with("user-1", "job-1")
    assert result == mock_job_repo.get_job.return_value



def test_post_job_execution_creates_execution_and_saves(job_service, mock_job_repo):
    execution_id = "job-1#exec-1"

    result = job_service.post_job_execution("job-1", execution_id)

    mock_job_repo.post_job_execution.assert_called_once()

    args, _ = mock_job_repo.post_job_execution.call_args
    passed_job_id, execution_model = args

    assert passed_job_id == "job-1"
    assert isinstance(execution_model, ExecutionModel)
    assert execution_model.execution_id == execution_id
    assert execution_model.job_id == "job-1"
    assert execution_model.status == ExecutionStatus.STARTED
    assert execution_model.max_retries == 3
    assert execution_model.started_at is not None

    assert result == execution_id



def test_update_job_execution_calls_repo(job_service, mock_job_repo):
    job_service.update_job_execution(
        job_id="job-1",
        execution_id="exec-1",
        status=ExecutionStatus.SUCCESS,
        log_url="s3://log",
        retry_count=1,
        finished_at="2025-01-01T00:00:00Z",
    )

    mock_job_repo.update_job_execution.assert_called_once_with(
        "job-1",
        "exec-1",
        ExecutionStatus.SUCCESS,
        1,
        "2025-01-01T00:00:00Z",
        "s3://log",
    )




def test_get_job_execution_calls_repo(job_service, mock_job_repo):
    mock_job_repo.get_job_execution.return_value = MagicMock()

    result = job_service.get_job_execution("job-1", "exec-1")

    mock_job_repo.get_job_execution.assert_called_once_with("job-1", "exec-1")
    assert result == mock_job_repo.get_job_execution.return_value