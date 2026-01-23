from fastapi.responses import JSONResponse
from fastapi.encoders  import jsonable_encoder
from typing import Any

class Response:

    @classmethod
    def success_response(cls, data : Any , message : str, status_code : int , by_alias:bool= True) -> JSONResponse:
        return JSONResponse(
            status_code= status_code,
            content={
                "status" : "success",
                "message" : message , 
                "data": jsonable_encoder(data, by_alias=by_alias)
            }
        )

    @classmethod
    def error_response(cls, message : str , status_code : int , error_code:str)->JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "fail",
                "message": message,
                "data": jsonable_encoder(None),
                "errorcode ": error_code,
            },
        )
