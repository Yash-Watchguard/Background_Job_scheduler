from pydantic import BaseModel, Field
from enums.schedule_type import ScheduleType

class Schedule(BaseModel):
    schedule_type: ScheduleType = Field(alias="ScheduleType")
    value: str = Field(alias="ScheduleValue")