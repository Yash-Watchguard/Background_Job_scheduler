from pydantic import BaseModel , Field, field_validator, ConfigDict
from enums.job_type import JobType
from enums.schedule_type import ScheduleType
from enums.task_type import TaskType
from models.task_input_model import TaskInput
from datetime import timezone, datetime
from errors.error_registry import ErrorCode
from errors.app_exception import AppException
from croniter import croniter

class JobReqest(BaseModel):
    job_type:JobType = Field(...)
    schedule_type:ScheduleType = Field(...)
    schedule_time:str = Field(...)
    task_type:TaskType = Field(...)
    task_input:TaskInput = Field(...)
    
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )
    
    @field_validator("schedule_time",mode="after")
    @classmethod
    def validate_date(cls,schedule_time:str,info):
        schedule_type = info.data.get("schedule_type")
        current_time = datetime.now(timezone.utc)
        if schedule_type == ScheduleType.At:
            try:
                scheduled_time = datetime.fromisoformat(schedule_time)
                
                if scheduled_time.tzinfo is None:
                    scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)
                
                if scheduled_time <= current_time:
                    raise AppException(error_code=ErrorCode.INVALID_SCHEDULE_TIME)
            except Exception:
                raise AppException(error_code=ErrorCode.INVALID_SCHEDULE_TIME)
        else:
            try:
                fields = schedule_time.split()
                if len(fields) != 6:
                    raise AppException(error_code=ErrorCode.INVALID_SCHEDULE_TIME)

                normalized_cron = schedule_time.replace("?", "*")

                cron_with_seconds = f"0 {normalized_cron}"

                itr = croniter(cron_with_seconds, current_time)
                print(itr)
                next_execution = itr.get_next(datetime)
                print(next_execution)
                

                if next_execution <= current_time:
                    raise AppException(error_code=ErrorCode.INVALID_SCHEDULE_TIME)
            except Exception:
                raise AppException(error_code=ErrorCode.INVALID_SCHEDULE_TIME)
            
        return schedule_time
    
    
            
                
            
            
            
    
    
    
    
    