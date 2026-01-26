from enum import Enum

class ScheduleType(str,Enum):
    At = "AT"
    CRON = "CRON"
    INTERVAL = "INTERVAL"