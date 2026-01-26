import jwt,time, os
from jwt import PyJWTError

from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from models.jwt_payload import JwtPayload
from errors.app_exception import AppException
from errors.error_registry import ErrorCode
from fastapi import Depends



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
        raise AppException(error_code=ErrorCode.INVALID_TOKEN) from exception