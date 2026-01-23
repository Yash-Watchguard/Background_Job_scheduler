from fastapi import FastAPI,status
from fastapi import HTTPException, Request
from response.response import Response
from constants.custom_error_code_registry import Python_Error,  Validation_Error
from errors.app_exception import AppException
from fastapi.exceptions import ValidationException,RequestValidationError

def register_exception_handler(app:FastAPI):
    @app.exception_handler(HTTPException)
    def http_exception_handler(req: Request, exc: HTTPException):
        return Response.error_response(
            message=exc.detail, 
            status_code=exc.status_code, 
            error_code=Python_Error
        )


    @app.exception_handler(AppException)
    def app_exception_handler(req: Request, exc: AppException):
        return Response.error_response(
            message=exc.message,
            status_code=exc.status_code, 
            error_code=exc.error_code
        )


    @app.exception_handler(ValidationException)
    def app_validation_expeption_handler(request: Request, exception: ValidationException):
        return Response.error_response(
            message=str(exception),
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code=Validation_Error,
        )
        
    @app.exception_handler(RequestValidationError)
    def app_request_validation_expeption_handler(request: Request, exception: ValidationException):
        return Response.error_response(
            message=str(exception),
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code=Validation_Error,
        )
        
    @app.exception_handler(Exception)
    def global_exception_handler(request: Request, exception: Exception):
        return Response.error_response(
            message="Internal Server Error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=Python_Error,
        )
