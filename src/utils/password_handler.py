from passlib.context import CryptContext

pwd_handle = CryptContext(
    schemes=["bcrypt"],
    deprecated= "auto"
)

def hash_password(pswd: str):
    
    return pwd_handle.hash(pswd)

def verify_password(plain_pswd: str, hashed_pswd: str):

    return pwd_handle.verify(plain_pswd, hashed_pswd)