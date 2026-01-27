import pytest


from enums.execution_status import ExecutionStatus
from models.job_execution_model import ExecutionModel
from unittest.mock import MagicMock


@pytest.fixture
def sqs_event_first_attempt():
    return {
        "Records": [
            {
                "messageId": "msg-1",
                "body": '{"job_id":"job-1","user_id":"user-1"}',
                "attributes": {
                    "ApproximateReceiveCount": "1"
                }
            }
        ]
    }


@pytest.fixture
def sqs_event_retry():
    return {
        "Records": [
            {
                "messageId": "msg-1",
                "body": '{"job_id":"job-1","user_id":"user-1"}',
                "attributes": {
                    "ApproximateReceiveCount": "2"
                }
            }
        ]
    }
