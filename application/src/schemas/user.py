from pydantic import BaseModel,Field , field_validator , EmailStr , ConfigDict
import re
from fastapi.exceptions import ValidationException

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{12,}$")
from pydantic import BaseModel,ConfigDict,EmailStr,Field


class LoginRequest(BaseModel):
    email:EmailStr = Field(...)
    password:str = Field(...)
    

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )
    
    
class SignupRequest(BaseModel):
    name: str = Field(min_length=1 , max_length=26 ,alias="name")
    email: EmailStr = Field(alias="email")
    
    password: str
    phone_number: str = Field(min_length=10 , max_length=10 , pattern=r"^[6-9][0-9]{9}$" , alias="phonenumber")
    
    @field_validator("password", mode="plain")
    def validate_password( password:str):
        if not PASSWORD_REGEX.match(password):
            raise ValidationException(
                "Password must contain atlease one uppercase character , one digit , one special character like (@, # , $) or minimum length should be 12 char"
            )
        return password
    
    model_config = ConfigDict(
        populate_by_name=True,
        extra= "forbid",
        str_strip_whitespace=True
    )
    