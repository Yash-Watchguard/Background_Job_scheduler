from enum import Enum

class JobType(str, Enum):
    ONE_TIME = "ONE_TIME"
    RECURRING = "RECURRING"
