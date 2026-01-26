from typing import Optional
from errors.error_registry import ERROR_REGISTRY
from fastapi import status

class AppException(Exception):
    def __init__(self, error_code:int, message:Optional[str]= None,detail:Optional[str]=None):
        error_info = ERROR_REGISTRY.get(error_code,{})
        self.error_code = error_code
        
        self.status_code = error_info.get("status_code",status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.message = error_info.get("message","Something Went Wrong")
        self.detail = detail