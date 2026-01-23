import bcrypt 


def check_password(input_password:str,hash_password:str)->bool:
    return bcrypt.checkpw(input_password.encode(),hash_password.encode())

def generate_hash_password(input_password:str):
    hashed =  bcrypt.hashpw(input_password.encode(),bcrypt.gensalt())

    return hashed.decode()