import jwt,time, os
from jwt.exceptions import PyJWTError

from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from models.jwt_payload import JwtPayload
from errors.app_exception import AppException
from errors.error_registry import ErrorCode
from fastapi import Depends
from core.config import algo, secret_key, expiry_time



security = HTTPBearer() 

def create_jwt_token(user_id: str) -> str:
    
   
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
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token,secret_key,algorithms=[algo])
        return JwtPayload(**payload)
        
    except PyJWTError as exception:
        raise AppException(error_code=ErrorCode.INVALID_TOKEN) from exception