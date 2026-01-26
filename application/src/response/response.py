from fastapi.responses import JSONResponse
from fastapi.encoders  import jsonable_encoder
from typing import Any,Optional

class Response:

    @classmethod
    def success_response(cls , message : str, status_code : int , by_alias:bool= True, data : Optional[Any]=None) -> JSONResponse:
        return JSONResponse(
            status_code= status_code,
            content={
                "status" : "success",
                "message" : message , 
                "data": jsonable_encoder(data, by_alias=by_alias)
            }
        )

    @classmethod
    def error_response(cls, message : str , status_code : int , error_code:str,detail:Optional[str]=None)->JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "fail",
                "message": message,
                "detail": detail,
                "errorcode ": error_code,
            },
        )
