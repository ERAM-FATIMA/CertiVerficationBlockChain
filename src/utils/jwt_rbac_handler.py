from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "certiveri_super_secret_key"
ALGORITHM = "HS256"
TOKEN_EXPIRY_MIN = 60

def create_token(user_id: int, role: str):

    expiry = datetime.now() + timedelta(minutes=TOKEN_EXPIRY_MIN)

    payload = {
        "user_id" : user_id,
        "role" : role,
        "exp" : expiry
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise JWTError
    

