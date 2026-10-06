from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import hashlib

from src.database.dbase import get_db
from src.models.all_models import Employer
from src.schemas.employer_schema import EmployerRegister, EmployerLogin
from src.utils.password_handler import hash_password, verify_password
from src.utils.jwt_rbac_handler import create_token
from src.utils.auth_dependency import get_cur_user
from src.BlockChainLocal.blockchain_instance import blockchain

router = APIRouter(
    prefix="/employer",
    tags=["Employer"]
)

@router.post("/register", status_code=201)
def register_employer(indata: EmployerRegister, db: Session = Depends(get_db)):

    exists_emp = db.query(Employer).filter(Employer.email == indata.email).first()

    if exists_emp:
        raise HTTPException(status_code=400, detail="Employer already exists")

    hashed_pw = hash_password(indata.password)

    new_emp = Employer(
        name=indata.name,
        email=indata.email,
        password=hashed_pw
    )

    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return {
        "msg": "Employer registered",
        "employer_id": new_emp.id
    }

@router.post("/login")
def login_employer(data: EmployerLogin, db: Session = Depends(get_db)):

    emp = db.query(Employer).filter(Employer.email == data.email).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employer not found")

    if not verify_password(data.password, emp.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token(
        user_id=emp.id,
        role="employer"
    )

    return {
        "msg": "Employer login successful!!",
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/verify-certificate")
async def verify_cert(file: UploadFile = File(...), cur_user = Depends(get_cur_user)):

    if cur_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Only employers allowed!")
    
    file_bytes = await file.read()
    uploaded_hash = hashlib.sha256(file_bytes).hexdigest()

    result = blockchain.verify_certificate(uploaded_hash)

    return result