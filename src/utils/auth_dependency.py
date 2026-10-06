from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.jwt_rbac_handler import verify_token

security = HTTPBearer()

def get_cur_user(cred: HTTPAuthorizationCredentials = Depends(security)):

    token = cred.credentials

    try: 
        payload = verify_token(token)
        return{
            "user_id" : payload["user_id"],
            "role": payload["role"]
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Token expired or invalid!")
