from fastapi import APIRouter

from services.auth_service import AuthService
from schemas.user import LoginRequest,SignupRequest
from fastapi import APIRouter, Depends
from http import HTTPStatus
from response.response import Response
from services.auth_service import AuthService
from dpendencies.auth_dependecy import get_auth_service
from models.user_model import User

auth_router = APIRouter()

@auth_router.post("/v1/auth/login")
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):

    login_response = auth_service.login(request.email, request.password)
    return Response.success_response(
        data=login_response,
        message="Token generated Successfully",
        status_code=HTTPStatus.CREATED.value,
    )


@auth_router.post("/v1/auth/signup")
async def signup(
    request: SignupRequest,
    auth_srvice: AuthService = Depends(get_auth_service),
):

    response: User = auth_srvice.signup(user_details=request)

    return Response.success_response(
        data=response,
        status_code=HTTPStatus.CREATED,
        message="user signup successfully",
    )