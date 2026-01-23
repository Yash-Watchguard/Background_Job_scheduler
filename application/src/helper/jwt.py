import jwt
import time

import os
from models.jwt_payload import JwtPayload

from fastapi import Depends,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jwt import PyJWTError
from errors.app_exception import AppException
from constants import custom_error_code_registry



security = HTTPBearer() 

def create_jwt_token(user_id: str) -> str:
    
    secret_key: str = os.getenv("JWT_SECRET_KEY","yashgoyal123").encode('utf-8')
    algo: str = os.getenv("JWT_ALGORITHM")
    expiry_time: int = int(os.getenv("JWT_EXPIRY_TIME"))
    payload = JwtPayload(
        authorized= "true",       
        user_id= user_id,          
        exp=  int(time.time()) + (expiry_time * 3600)
        ).model_dump()

    token = jwt.encode(
        payload,
        secret_key.strip(),
        algorithm=algo
    )
    return token

def varify_jwt(credentials : HTTPAuthorizationCredentials= Depends(security))->JwtPayload:
    secret_key: str = os.getenv("JWT_SECRET_KEY").encode('utf-8')
    algo: str = os.getenv("JWT_ALGORITHM")
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token,secret_key,algorithms=[algo])
        return JwtPayload(**payload)
        
    except PyJWTError as exception:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, message="user is not authorized or invalid token" , error_code=custom_error_code_registry.Unauthorized_Error) from exception