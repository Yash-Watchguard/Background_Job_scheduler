from enum import Enum

class JobStatus(str, Enum):
    ACTIVE = "ACTIVE"
    IN_ACTIVE = "IN_ACTIVE"
    DELETE = "DELETE"