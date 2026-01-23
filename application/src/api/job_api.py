from fastapi import APIRouter , UploadFile , File , Form, Depends, status
from schemas.job import JobReqest
import json
from dpendencies.job_dependency import get_job_service
from services.job_service import JobService
from errors.app_exception  import AppException
from response.response import Response
from helper.jwt import varify_jwt
from models.jwt_payload import JwtPayload

job_router = APIRouter()


@job_router.post('/v1/job')
def create_job(job_data:JobReqest,job_service:JobService = Depends(get_job_service), jwt_payload:JwtPayload = Depends(varify_jwt) ):
    # first validate the request
    user_id = jwt_payload.user_id
    
    response = job_service.create_job(job_data, user_id)
    
    return Response.success_response(status_code=status.HTTP_201_CREATED, message="bg job scheduled successfully", data="response")
    
    
