from enums.schedule_type import ScheduleType
from enums.job_type import JobType
from errors.app_exception import AppException
from constants.error_messages import schedule_mismatch_error
from constants.custom_error_code_registry import scheduled_mismatch
from fastapi import status

def validate_schedule(scheduled_type:ScheduleType, job_type:JobType):
    if job_type == JobType.ONE_TIME:
        if scheduled_type != ScheduleType.At:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, message=schedule_mismatch_error, error_code=scheduled_mismatch)
        
    if job_type == JobType.RECURRING:
        if scheduled_type == ScheduleType.At:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, message=schedule_mismatch_error, error_code=scheduled_mismatch)
        