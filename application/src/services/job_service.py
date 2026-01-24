
from services.scheduler_service import SchedulerService
from repositories.job_repo import JobRepo
from schemas.job import JobReqest
from fastapi import UploadFile
from helper.generate_uuid import generate_uuid
from core.config import JOB_QUEUE_ARN
from helper.validate_schedule import validate_schedule
from helper.get_schedule_expression import get_schedule_expression

class JobService:
    def __init__(self,job_repo :JobRepo , scheduler_service:SchedulerService):
        self.job_repo = job_repo
        self.scheduler_service = scheduler_service
        
    def create_job(self, job_data:JobReqest, user_id:str):
        # then call the eventbridge service
        job_id = generate_uuid()
        
        try:
            # varify the schedue
            print(job_data.schedule_type)
            validate_schedule(job_data.schedule_type, job_data.job_type)
            schedule_expression = get_schedule_expression(job_data.schedule_type, job_data.schedule_value)
            self.scheduler_service.create_new_schedule(job_id,user_id,JOB_QUEUE_ARN,schedule_expression)
        except Exception:
            raise 
        
        # store the job in ddb
        
        try:
            self.job_repo.put_new_job(job_id,user_id,job_data)
        except Exception:
            raise
        
        
