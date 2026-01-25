from pydantic import BaseModel

class ExecutionDto(BaseModel):
    execution_id:str
    status:str
    retry_count:int
    log_url:str
    started_at:str
    finished_at:str