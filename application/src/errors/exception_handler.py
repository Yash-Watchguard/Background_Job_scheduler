from fastapi import FastAPI,status
from fastapi import HTTPException, Request
from response.response import Response

from errors.app_exception import AppException
from fastapi.exceptions import ValidationException,RequestValidationError
from errors.error_registry import ErrorCode , ERROR_REGISTRY

def register_exception_handler(app:FastAPI):
    @app.exception_handler(HTTPException)
    def http_exception_handler(req: Request, exc: HTTPException):
        return Response.error_response(
            message=ERROR_REGISTRY.get(ErrorCode.PYTHON_EXECUTION_ERROR).get("message"),
            status_code=exc.status_code, 
            error_code=ErrorCode.PYTHON_EXECUTION_ERROR,
            detail=exc.detail
        )


    @app.exception_handler(AppException)
    def app_exception_handler(req: Request, exc: AppException):
        return Response.error_response(
            message=exc.message,
            status_code=exc.status_code, 
            error_code=exc.error_code,
            detail=exc.detail
        )


    @app.exception_handler(ValidationException)
    def app_validation_expeption_handler(request: Request, exception: ValidationException):
        return Response.error_response(
            message=ERROR_REGISTRY.get(ErrorCode.VALIDATION_ERROR).get("message"),
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code=ErrorCode.VALIDATION_ERROR,
            detail=str(exception)
        )
        
    @app.exception_handler(RequestValidationError)
    def app_request_validation_expeption_handler(request: Request, exception: ValidationException):
        return Response.error_response(
            message=ERROR_REGISTRY.get(ErrorCode.VALIDATION_ERROR).get("message"),
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code=ErrorCode.VALIDATION_ERROR,
            detail=str(exception)
        )
        
    @app.exception_handler(Exception)
    def global_exception_handler(request: Request, exception: Exception):
        return Response.error_response(
            message=ERROR_REGISTRY.get(ErrorCode.INTERNAL_SERVER_ERROR).get("message"),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        )
