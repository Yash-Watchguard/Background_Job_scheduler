
from models.user_model import User
from errors.app_exception import AppException

from helper.jwt import create_jwt_token
from helper.hashed_check_password import check_password,generate_hash_password

from schemas.user import SignupRequest
from helper.generate_uuid import generate_uuid
from repositories.user_repo import UserRepo
from errors.error_registry import ErrorCode


class AuthService:
    
    def __init__(self,user_repo:UserRepo):
        self.user_repo = user_repo
        
    def login(self,email:str, password:str ):
        
        response: User= self.user_repo.get_user_by_email(email=email)
        

        if not check_password(password,response.password):
            raise AppException(error_code=ErrorCode.INVALID_CREDENTIAL)

        jwt_token = create_jwt_token(response.id)
        

        return {"UserId": response.id, "token": jwt_token}
    
    
    def signup(self, user_details: SignupRequest) -> User:
        
        user: User = self.user_repo.get_user_by_email(user_details.email)
        if user :
            raise AppException(error_code=ErrorCode.USER_ALREADY_PRESENT)

            
        user_id = generate_uuid()
        
        user: User = User(
            Id=user_id,
            Email=user_details.email,
            Name=user_details.name,
            PhoneNumber=user_details.phone_number,
            Password= generate_hash_password(user_details.password)
        )

        self.user_repo.save_user(user)
        

        return user