from unittest.mock import patch

from services.log_service import LogService


@patch("services.log_service.s3")
@patch("services.log_service.LOG_BUCKET", "test-log-bucket")
def test_upload_log_success(mock_s3):
    service = LogService()

    job_id = "job-1"
    execution_id = "exec-1"
    logs = "this is a test log"

    result = service.upload_log(
        job_id=job_id,
        execution_id=execution_id,
        logs=logs
    )

    expected_key = "job_id=job-1/execution_id=exec-1.log"

    mock_s3.put_object.assert_called_once_with(
        Bucket="test-log-bucket",
        Key=expected_key,
        Body=logs.encode("utf-8"),
        ContentType="text/plain",
    )

    assert result == f"s3://test-log-bucket/{expected_key}"
