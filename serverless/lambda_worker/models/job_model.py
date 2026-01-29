from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from enums.job_type import JobType
from enums.schedule_type import ScheduleType
from enums.task_type import TaskType
from models.task_input import TaskInput


class JobRecord(BaseModel):
    job_id: str = Field(alias="JobId")
    job_type: JobType = Field(alias="JobType")
    schedule_type: ScheduleType = Field(alias="ScheduleType")
    schedule_time: str = Field(alias="ScheduleValue")
    task_type:TaskType = Field(alias="TaskType")
    task_input:TaskInput = Field(alias="TaskInput")
    created_at: datetime = Field(alias="CreatedAt")
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True
    )

    
    
    
    