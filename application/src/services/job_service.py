from typing import List

from fastapi import status

from services.scheduler_service import SchedulerService
from repositories.job_repo import JobRepo
from schemas.job import JobReqest
from helper.generate_uuid import generate_uuid
from core.config import JOB_QUEUE_ARN
from helper.validate_schedule import validate_schedule
from helper.get_schedule_expression import get_schedule_expression
from models.job_execution_model import ExecutionModel
from errors.app_exception import AppException
from enums.job_status import JobStatus
from models.job_model import JobRecord
from errors.error_registry import ErrorCode

class JobService:
    def __init__(self,job_repo :JobRepo , scheduler_service:SchedulerService):
        self.job_repo = job_repo
        self.scheduler_service = scheduler_service
        
    def create_job(self, job_data:JobReqest, user_id:str):
        
        job_id = generate_uuid()
        
        
        validate_schedule(job_data.schedule_type, job_data.job_type)
        
        schedule_expression = get_schedule_expression(job_data.schedule_type, job_data.schedule_value)
        
        self.scheduler_service.create_new_schedule(job_id,user_id,JOB_QUEUE_ARN,schedule_expression)
        
    
        self.job_repo.put_new_job(job_id,user_id,job_data)
        
        
    def get_scheduled_job(self,user_id , job_id)->JobRecord:
        return self.job_repo.get_job(user_id,job_id)
        
        
    def get_job_executions(self, job_id)->List[ExecutionModel]:
        return self.job_repo.get_job_executions(job_id)
    
    def delete_job(self , job_id:str , user_id:str):
        
        try:
            job= self.job_repo.get_job(user_id, job_id)
            if job.created_by != user_id:
                raise AppException(error_code=ErrorCode.UNAUTHORIZED)
        except AppException as exception:
            raise AppException(error_code=ErrorCode.JOB_NOT_FOUND, detail=exception.detail)
        

        self.scheduler_service.delete_scheduler(job_id)
        
    
        self.job_repo.update_job_status(user_id,job_id,JobStatus.DELETE.value)
        
    def deactivate_job(self, job_id:str, user_id:str):
        
        try:
            job= self.job_repo.get_job(user_id, job_id)
            if job.created_by != user_id:
                raise AppException(error_code=ErrorCode.UNAUTHORIZED)
        except AppException as exception:
            raise AppException(error_code=ErrorCode.JOB_NOT_FOUND, detail=exception.detail)
        
        
        self.scheduler_service.deacivate_scheduler(job_id)
        
        self.job_repo.update_job_status(user_id, job_id, JobStatus.IN_ACTIVE.value)
        
    def activate_job(self , job_id:str , user_id:str):
        
        try:
            job= self.job_repo.get_job(user_id, job_id)
            if job.created_by != user_id:
                raise AppException(error_code=ErrorCode.UNAUTHORIZED)
        except AppException as exception:
            raise AppException(error_code=ErrorCode.JOB_NOT_FOUND, detail=exception.detail)
        
        
        self.scheduler_service.activate_scheduler(job_id)
        

        self.job_repo.update_job_status(user_id, job_id, JobStatus.ACTIVE.value)
        
        
        
    
            
            
