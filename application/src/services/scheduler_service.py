import json
from errors.app_exception import AppException
from fastapi import status

class SchedulerService:
    def __init__(self, scheduler_client, event_bridge_role_arn:str,schedule_group_name:str ):
        self.scheduler_client = scheduler_client
        self.role_arn = event_bridge_role_arn
        self.group_name = schedule_group_name
        
        
    def create_new_schedule(self, job_id:str,user_id, target_queue_arn:str, schedule_expression:str):
        
        schedule_name = f"bg-job-{job_id}"
        
        try:
            response = self.scheduler_client.create_schedule(
            Name = schedule_name,
            GroupName = self.group_name,
            ScheduleExpression = schedule_expression,
            FlexibleTimeWindow={
                "Mode": "OFF"
            },
            Target = {
                "Arn" :target_queue_arn,
                "RoleArn": self.role_arn,
                "Input":json.dumps({
                    "job_id":job_id,
                    "user_id":user_id
                })
            }
        )
        
        except Exception as exception:
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message=f"error in eventbridge {exception}", error_code="1001")
        
        return response
    
    
    def delete_scheduler(self, job_id:str):
        
        schedule_name = f"bg-job-{job_id}"
        
        try:
            self.scheduler_client.delete_schedule(
                Name=schedule_name,
                GroupName=self.group_name,
            )
            
        except self.scheduler_client.exceptions.ResourceNotFoundException:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Schedule not found",
                error_code=1001
            )
        except Exception as exception:
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"error in delete the schedule{exception} ", error_code=1001) from exception
    
    def get_schedule_details(self, job_id:str):
        schedule_name = f"bg-job-{job_id}"
        
        try:
            response = self.scheduler_client.get_schedule(
                Name=schedule_name,
                GroupName=self.group_name,
            )
            return {
                "schedule_expression": response.get("ScheduleExpression"),
                "target": response.get("Target")
            }
        except self.scheduler_client.exceptions.ResourceNotFoundException:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Schedule not found",
                error_code=1001
            )
        except Exception as exception:
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"error in fetching the schedule{exception} ", error_code=1001) from exception
        
    def deacivate_scheduler(self, job_id:str):
        schedule_name = f"bg-job-{job_id}"
        
        try:
            schedule_details = self.get_schedule_details(job_id)
            self.scheduler_client.update_schedule(
                Name=schedule_name,
                GroupName=self.group_name,
                State="DISABLED",
                ScheduleExpression=schedule_details["schedule_expression"],
                Target=schedule_details["target"],
                FlexibleTimeWindow={"Mode": "OFF"},
            )
        except self.scheduler_client.exceptions.ResourceNotFoundException:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Schedule not found",
                error_code=1001
            )
        except Exception as exception:
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"error in updating the schedule{exception} ", error_code=1001) from exception
    
    def activate_scheduler(self, job_id:str):
        schedule_name = f"bg-job-{job_id}"
        
        try:
            schedule_details = self.get_schedule_details(job_id)
            self.scheduler_client.update_schedule(
                Name=schedule_name,
                GroupName=self.group_name,
                State="ENABLED",
                ScheduleExpression=schedule_details["schedule_expression"],
                Target=schedule_details["target"],
                FlexibleTimeWindow={"Mode": "OFF"},
            )    
        except self.scheduler_client.exceptions.ResourceNotFoundException:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Schedule not found",
                error_code=1001
            )
            
        except Exception as exception:
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"error in updating the schedule{exception} ", error_code=1001) from exception
       