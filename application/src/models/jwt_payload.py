from pydantic import BaseModel


class JwtPayload(BaseModel):
    authorized: str
    user_id: str         
    exp: int