from services.execution_logger import ExecutionLogger


def test_log_single_message():
    logger = ExecutionLogger()

    logger.log("hello world")

    logs = logger.get_logs()

    assert "hello world" in logs
    assert logs.startswith("[")
    assert logs.endswith("\n")


def test_log_multiple_messages():
    logger = ExecutionLogger()

    logger.log("first")
    logger.log("second")

    logs = logger.get_logs()

    assert "first" in logs
    assert "second" in logs
    assert logs.count("\n") == 2


def test_get_logs_initially_empty():
    logger = ExecutionLogger()

    logs = logger.get_logs()

    assert logs == ""
