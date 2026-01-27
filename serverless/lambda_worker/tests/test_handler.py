import pytest
from unittest.mock import patch, MagicMock, ANY

from handler import handler
from enums.execution_status import ExecutionStatus



@patch("handler.ExecutionLogger")
@patch("handler.job_service")
@patch("handler.email_service")
@patch("handler.log_service")
def test_handler_first_execution_success(
    mock_log_service,
    mock_email_service,
    mock_job_service,
    mock_logger_cls,
    sqs_event_first_attempt
):
    logger = MagicMock()
    logger.get_logs.return_value = "logs"
    mock_logger_cls.return_value = logger

    mock_job_service.get_job_execution.return_value = None

    job = MagicMock()
    job.task_type = "EMAIL"
    job.task_input.to = ["a@gmail.com"]
    job.task_input.sender_email = "sender@gmail.com"
    job.task_input.subject = "test"
    job.task_input.content = "hello"

    mock_job_service.get_job.return_value = job
    mock_log_service.upload_log.return_value = "s3://log-url"

    handler(sqs_event_first_attempt, None)

    mock_job_service.post_job_execution.assert_called_once()
    mock_email_service.send_email.assert_called_once()

    mock_job_service.update_job_execution.assert_called_with(
        job_id="job-1",
        execution_id="job-1#msg-1",
        status=ExecutionStatus.SUCCESS,
        log_url="s3://log-url",
        retry_count=None,
        finished_at=ANY
    )



@patch("handler.ExecutionLogger")
@patch("handler.job_service")
@patch("handler.email_service")
@patch("handler.log_service")
def test_handler_retry_execution(
    mock_log_service,
    mock_email_service,
    mock_job_service,
    mock_logger_cls,
    sqs_event_retry
):
    logger = MagicMock()
    logger.get_logs.return_value = "logs"
    mock_logger_cls.return_value = logger

    mock_job_service.get_job_execution.return_value = MagicMock()

    job = MagicMock()
    job.task_type = "EMAIL"
    job.task_input.to = ["a@gmail.com"]
    job.task_input.sender_email = "sender@gmail.com"
    job.task_input.subject = "test"
    job.task_input.content = "hello"

    mock_job_service.get_job.return_value = job
    mock_log_service.upload_log.return_value = "s3://log-url"

    handler(sqs_event_retry, None)

    mock_job_service.update_job_execution.assert_any_call(
        job_id="job-1",
        execution_id="job-1#msg-1",
        status=ExecutionStatus.IN_PROGRESS,
        log_url=None,
        retry_count=1,
        finished_at=None
    )



@patch("handler.ExecutionLogger")
@patch("handler.job_service")
@patch("handler.email_service")
@patch("handler.log_service")
def test_handler_failure(
    mock_log_service,
    mock_email_service,
    mock_job_service,
    mock_logger_cls,
    sqs_event_first_attempt
):
    logger = MagicMock()
    logger.get_logs.return_value = "logs"
    mock_logger_cls.return_value = logger

    mock_job_service.get_job_execution.return_value = None

    job = MagicMock()
    job.task_type = "EMAIL"
    job.task_input.to = ["a@gmail.com"]
    job.task_input.sender_email = "sender@gmail.com"
    job.task_input.subject = "test"
    job.task_input.content = "hello"

    mock_job_service.get_job.return_value = job
    mock_email_service.send_email.side_effect = Exception("SMTP failed")
    mock_log_service.upload_log.return_value = "s3://log-url"

    with pytest.raises(Exception):
        handler(sqs_event_first_attempt, None)

    mock_job_service.update_job_execution.assert_called_with(
        job_id="job-1",
        execution_id="job-1#msg-1",
        status=ExecutionStatus.FAILED,
        log_url="s3://log-url",
        retry_count=None,
        finished_at=ANY
    )
