from services.auth_service import AuthService
from dpendencies.user_dependency import get_user_repo
from repositories.user_repo import UserRepo
from fastapi import Depends


def get_auth_service(user_repo:UserRepo =Depends(get_user_repo))->AuthService:
    return AuthService(user_repo)