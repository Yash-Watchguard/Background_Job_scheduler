from pydantic import BaseModel,Field, ConfigDict,EmailStr


class User(BaseModel):
    name:str = Field(alias="Name")
    id:str = Field(alias="Id")
    email:EmailStr = Field(alias="Email")
    password:str= Field(alias="Password")
    phone_number:str= Field(alias="PhoneNumber")
    
    model_config= ConfigDict(
        populate_by_name = True
    )