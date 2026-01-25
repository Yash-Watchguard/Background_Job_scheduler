
from services.scheduler_service import SchedulerService
from repositories.job_repo import JobRepo
from schemas.job import JobReqest
from fastapi import status
from helper.generate_uuid import generate_uuid
from core.config import JOB_QUEUE_ARN
from helper.validate_schedule import validate_schedule
from helper.get_schedule_expression import get_schedule_expression
from models.job_execution_model import ExecutionModel
from typing import List
from errors.app_exception import AppException
from enums.job_status import JobStatus
from models.job_model import JobRecord

class JobService:
    def __init__(self,job_repo :JobRepo , scheduler_service:SchedulerService):
        self.job_repo = job_repo
        self.scheduler_service = scheduler_service
        
    def create_job(self, job_data:JobReqest, user_id:str):
        
        job_id = generate_uuid()
        
        try:
            print(job_data.schedule_type)
            validate_schedule(job_data.schedule_type, job_data.job_type)
            schedule_expression = get_schedule_expression(job_data.schedule_type, job_data.schedule_value)
            self.scheduler_service.create_new_schedule(job_id,user_id,JOB_QUEUE_ARN,schedule_expression)
        except Exception as execption:
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message=str(execption), error_code=1001) from execption
        
    
        self.job_repo.put_new_job(job_id,user_id,job_data)
        
        
    def get_scheduled_job(self,user_id , job_id)->JobRecord:
        return self.job_repo.get_job(user_id,job_id)
        
        
    def get_job_executions(self, job_id)->List[ExecutionModel]:
        return self.job_repo.get_job_executions(job_id)
    
    def delete_job(self , job_id:str , user_id:str):
        
        try:
            _= self.job_repo.get_job(user_id, job_id)
        except Exception as e:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, message="either user is unautorized or job is not present",error_code=1001)
        
        try:
            self.scheduler_service.delete_scheduler(job_id)
        except Exception as exception:
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Job Deletetion Failed due to f{exception}", error_code=1001)
    
        self.job_repo.update_job_status(user_id,job_id,JobStatus.DELETE.value)
        
    def deactivate_job(self, job_id:str, user_id:str):
        
        try:
            _= self.job_repo.get_job(user_id, job_id)
        except Exception as e:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, message="either user is unautorized or job is not present")
        
        
        self.scheduler_service.deacivate_scheduler(job_id)
        
        try:
            self.job_repo.update_job_status(user_id, job_id, JobStatus.IN_ACTIVE.value)
        except AppException as e:
            raise AppException(status_code=e.status_code, message="Schedule deactivate process failed", error_code=1001)
        
    def activate_job(self , job_id:str , user_id:str):
        try:
            _= self.job_repo.get_job(user_id, job_id)
        except Exception as e:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, message="either user is unautorized or job is not present")
        
        
        self.scheduler_service.activate_scheduler(job_id)
        
        try:
            self.job_repo.update_job_status(user_id, job_id, JobStatus.ACTIVE.value)
        except AppException as e:
            raise AppException(status_code=e.status_code, message="Schedule activate process failed", error_code=1001)
        
        
    
            
            
