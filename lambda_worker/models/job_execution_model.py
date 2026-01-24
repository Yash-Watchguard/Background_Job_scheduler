from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enums.execution_status import ExecutionStatus
from datetime import datetime

class ExecutionModel(BaseModel):
    execution_id:str = Field(alias="ExecutionId")
    job_id:str = Field(alias="JobId")
    status:ExecutionStatus = Field(alias="Status")
    retry_count:int = Field(default=0,alias="RetryCount")
    max_retries:int = Field(alias="MaxRetries")
    log_url:Optional[str] = Field(default=None, alias="LogUrl")
    started_at:datetime = Field(alias="StartedAt")
    finished_at:Optional[datetime] = Field(default=None, alias="FinishedAt")
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    