from enums.schedule_type import ScheduleType
from enums.job_type import JobType
from errors.app_exception import AppException
from errors.error_registry import ErrorCode

def validate_schedule(scheduled_type:ScheduleType, job_type:JobType):
    if job_type == JobType.ONE_TIME:
        if scheduled_type != ScheduleType.At:
            raise AppException(error_code=ErrorCode.SCHEDULE_JOB_TYPE_MISMATCH)
        
    if job_type == JobType.RECURRING:
        if scheduled_type == ScheduleType.At:
            raise AppException( error_code=ErrorCode.SCHEDULE_JOB_TYPE_MISMATCH)
        