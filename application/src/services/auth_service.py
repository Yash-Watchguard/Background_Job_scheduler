from services.user_service import UserService
from models.user_model import User
from errors.app_exception import AppException
from fastapi import status
from helper.jwt import create_jwt_token
from helper.hashed_check_password import check_password,generate_hash_password
from constants.custom_error_code_registry import Unauthorized_Error,Not_Found
from schemas.user import SignupRequest
from helper.generate_uuid import generate_uuid
from repositories.user_repo import UserRepo


class AuthService:
    
    def __init__(self,user_repo:UserRepo):
        self.user_repo = user_repo
        
    def login(self,email:str, password:str ):
        
        try:
            response: User= self.user_repo.get_user_by_email(email=email)
        except Exception as exception:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND,message="Invalid Email , Password user not available ", error_code=Not_Found) from exception

        if not check_password(password,response.password):
            raise AppException(status_code=status.HTTP_401_UNAUTHORIZED,message="Invalid Password , please check", error_code=Unauthorized_Error)

        jwt_token = create_jwt_token(response.id)
        

        return {"UserId": response.id, "token": jwt_token}
    
    
    def signup(self, user_details: SignupRequest) -> User:
        try:
            user: User = self.user_repo.get_user_by_email(user_details.email)
            if user :
                raise AppException(status_code=status.HTTP_409_CONFLICT,message="User Is Already Available with this email please try with another email",error_code=111)
        except AppException as exception:
            raise AppException(status_code=status.HTTP_409_CONFLICT,message="User Is Already Available with this email please try with another email",error_code=111) from exception
            
        user_id = generate_uuid()
        
        user: User = User(
            Id=user_id,
            Email=user_details.email,
            Name=user_details.name,
            Phonenumber=user_details.phone_number,
            Password= generate_hash_password(user_details.password)
        )

        
        self.user_repo.save_user(user)
        

        return user