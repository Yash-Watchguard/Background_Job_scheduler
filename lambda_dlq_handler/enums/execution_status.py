from enum import Enum

class ExecutionStatus(str, Enum):
    STARTED = "STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS= "SUCCESS"
    FAILED = "FAILED"
    PERMANENTLY_FAILED= "PERMANENTLY_FAILED"