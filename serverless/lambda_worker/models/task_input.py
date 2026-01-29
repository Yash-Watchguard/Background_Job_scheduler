from pydantic import BaseModel,Field, ConfigDict, EmailStr

class TaskInput(BaseModel):
    to:list[EmailStr] = Field(min_length=1,alias="To")
    sender_email:EmailStr = Field(alias="SenderEmail")
    subject:str = Field(alias="Subject")
    content:str = Field(alias="Content")
    
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True
    )
    