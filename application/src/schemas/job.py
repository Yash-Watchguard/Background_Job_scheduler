from pydantic import BaseModel , Field
from typing import Optional
from enums.job_type import JobType
from enums.schedule_type import ScheduleType
from enums.task_type import TaskType
from models.task_input import TaskInput

class JobReqest(BaseModel):
    job_type:JobType = Field(...)
    schedule_type:ScheduleType = Field(...)
    schedule_value:str = Field(...)
    task_type:TaskType = Field(...)
    task_input:TaskInput = Field(...)
    
    
    