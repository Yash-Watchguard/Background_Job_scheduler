from fastapi import APIRouter , UploadFile , File , Form, Depends, status
from schemas.job import JobReqest
import json
from dpendencies.job_dependency import get_job_service
from services.job_service import JobService
from errors.app_exception  import AppException
from response.response import Response
from helper.jwt import varify_jwt
from models.jwt_payload import JwtPayload
from schemas.job_execution_dto import ExecutionDto

job_router = APIRouter()


@job_router.post('/v1/job')
async def create_job(job_data:JobReqest,job_service:JobService = Depends(get_job_service), jwt_payload:JwtPayload = Depends(varify_jwt) ):
    # first validate the request
    user_id = jwt_payload.user_id
    
    job_service.create_job(job_data, user_id)
    
    return Response.success_response(status_code=status.HTTP_201_CREATED, message="bg job scheduled successfully", data=None)

@job_router.get('/v1/job/{job_id}')
async def get_job(job_id:str,jwt_payload:JwtPayload= Depends(varify_jwt), job_service:JobService = Depends(get_job_service)):
    user_id = jwt_payload.user_id
    
    job = job_service.get_scheduled_job(user_id,job_id)
    
    return Response.success_response(status_code=status.HTTP_200_OK,message="ok", data=job)

@job_router.get('/v1/jobs/{job_id}/executions')
async def get_all_job_executions(job_id:str,jwt_payload:JwtPayload= Depends(varify_jwt), job_service:JobService = Depends(get_job_service)):
    user_id = jwt_payload.user_id
    
    job_executions = job_service.get_job_executions(job_id)
    
    result:list[ExecutionDto]=[]
    
    for item in job_executions:
        execution_dto = ExecutionDto(
            execution_id=item.execution_id,
            status=item.status.value,
            retry_count=item.retry_count,
            log_url=item.log_url,
            started_at= item.started_at.isoformat(),
            finished_at=item.finished_at.isoformat()
        )
        result.append(execution_dto)
        
    return Response.success_response(data=result,message="executions fetched successfully", status_code=status.HTTP_200_OK)

@job_router.delete('/v1/job/{job_id}')
async def delete_job(job_id:str, jwt_payload:JwtPayload = Depends(varify_jwt), job_service:JobService=Depends(get_job_service)):
    user_id = jwt_payload.user_id
    
    job_service.delete_job(job_id,user_id)
    
    return Response.success_response(status_code=status.HTTP_200_OK,message="job deleted successfully" , data=None)


    
@job_router.patch('/v1/job/{job_id}/deactivate')
async def terminate_job(job_id:str, jwt_payload:JwtPayload = Depends(varify_jwt), job_service:JobService=Depends(get_job_service)):
    user_id = jwt_payload.user_id
    
    job_service.deactivate_job(job_id,user_id)
    
    return Response.success_response(status_code=status.HTTP_200_OK,message="job terminated successfully" , data=None)
    
    
@job_router.patch('/v1/job/{job_id}/activate')
async def activate_job(job_id:str, jwt_payload:JwtPayload = Depends(varify_jwt), job_service:JobService=Depends(get_job_service)):
    user_id = jwt_payload.user_id
    
    job_service.activate_job(job_id,user_id)
    
    return Response.success_response(status_code=status.HTTP_200_OK,message="job activates successfully" , data=None)   
