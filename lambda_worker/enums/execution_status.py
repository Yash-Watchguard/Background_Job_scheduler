from enum import Enum

class ExecutionStatus(str, Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"