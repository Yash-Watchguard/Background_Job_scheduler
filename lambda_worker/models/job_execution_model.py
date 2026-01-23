from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enums.execution_status import ExecutionStatus

class ExecutionModel(BaseModel):
    Execution_id:str = Field(alias="ExecutionId")
    job_id:str = Field(alias="JobId")
    status:ExecutionStatus = Field(alias="Status")
    log_url:Optional[str] = Field(default=None, alias="LogUrl")
    
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    