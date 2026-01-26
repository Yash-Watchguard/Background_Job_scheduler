from typing import Dict, Any
from fastapi import status
class ErrorCode:
    UNAUTHORIZED = 1001
    TOKEN_EXPIRED = 1003
    INVALID_TOKEN = 1004
    USER_NOT_FOUND = 1005
    INVALID_SCHEDULE_TIME = 1006
    SCHEDULED_JOB_NOT_PRESENT = 1007
    VALIDATION_ERROR = 1008
    INTERNAL_SERVER_ERROR = 1009
    PYTHON_EXECUTION_ERROR = 1010
    DB_ERROR = 1011
    INVALID_CREDENTIAL = 1012
    USER_ALREADY_PRESENT = 1013
    SCHEDULE_JOB_TYPE_MISMATCH =1014 
    JOB_CREATION_FAILED = 1015
    FAILED_TO_FETCH_JOB_EXECUTIONS = 1016
    JOB_NOT_FOUND = 1017
    JOB_DELETION_FAILED = 1018
    SCHEDULE_NOT_FOUND = 1019
    JOB_UPDATE_FAILED = 1020
    
    

ERROR_REGISTRY:Dict[int, Dict[str,Any]]={
    ErrorCode.UNAUTHORIZED: {
        "message":"unauthorized for perform this job",
        "status_code":status.HTTP_403_FORBIDDEN
    },
    ErrorCode.VALIDATION_ERROR:{
        "message":"Validation Error",
        "status_code":status.HTTP_422_UNPROCESSABLE_CONTENT
    },
    ErrorCode.INTERNAL_SERVER_ERROR:{
        "message" :"internal server error",
        "status_code" :status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    ErrorCode.PYTHON_EXECUTION_ERROR:{
        "message" : "pyhton execution error",
        "status_code" :status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    ErrorCode.USER_NOT_FOUND:{
        "message" : "User Not Found",
        "status_code":status.HTTP_404_NOT_FOUND
    },
    ErrorCode.DB_ERROR:{
        "message": "Error from the dynamo db",
        "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    ErrorCode.INVALID_CREDENTIAL:{
       "message":"Invalid Password , please check",
       "status_code":status.HTTP_403_FORBIDDEN
    },
    ErrorCode.USER_ALREADY_PRESENT:{
        "message" :"User Is Already Available with this email please try with another email",
        "status_code":status.HTTP_409_CONFLICT
    },
    ErrorCode.SCHEDULE_JOB_TYPE_MISMATCH:{
        "message":"schedule and job Type does not match",
        "status_code":status.HTTP_400_BAD_REQUEST
    },
    ErrorCode.JOB_CREATION_FAILED:{
        "message":"Job Creation Failed",
        "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
    ErrorCode.FAILED_TO_FETCH_JOB_EXECUTIONS:{
        "message" : "Error in fetching the executions of scheduled background job",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    ErrorCode.JOB_NOT_FOUND:{
        "message" : "job not present",
        "status_code": status.HTTP_404_NOT_FOUND
    },
    ErrorCode.JOB_DELETION_FAILED:{
        "message":"job deletion failed",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    ErrorCode.SCHEDULE_NOT_FOUND:{
        "message" : "schedule not found",
        "status_code":status.HTTP_404_NOT_FOUND
    },
    ErrorCode.JOB_UPDATE_FAILED:{
        "message" : "job update failed",
        "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    ErrorCode.INVALID_TOKEN:{
        "message": "Invalid token",
        "status_code":status.HTTP_401_UNAUTHORIZED
    }
    
    
}