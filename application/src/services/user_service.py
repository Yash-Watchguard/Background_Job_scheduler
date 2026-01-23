from repositories.user_repo import UserRepo
from models.user_model import User
class UserService:
    def __init__(self, user_repo:UserRepo):
        self.user_repo = user_repo
        
    def get_user_by_email(self, email:str)->User:
        pass