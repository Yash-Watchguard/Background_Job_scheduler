from job_repo import JobRepo
class JobService:
    def __init__(self,job_repo:JobRepo):
        self.job_repo = job_repo
        
    def update_execution_status(self, job_id:str , execution_id:str):
        return self.job_repo.update_job_execution(job_id, execution_id)