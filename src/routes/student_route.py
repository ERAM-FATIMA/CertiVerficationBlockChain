from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import os

from src.database.dbase import get_db
from src.models.all_models import Student, Certificates
from src.schemas.student_schema import StudentLogin, StudentRegister
from src.utils.password_handler import hash_password, verify_password
from src.utils.jwt_rbac_handler import create_token, verify_token
from src.utils.auth_dependency import get_cur_user

router = APIRouter(
    prefix="/student",
    tags=["Student"]
)

@router.post("/register", status_code=201)
def register_student(indata: StudentRegister, db: Session = Depends(get_db), cur_user = Depends(get_cur_user)):

    if cur_user["role"] != "university":
        raise HTTPException(status_code=403, detail="Only University allowed!")
    
    exist_std = db.query(Student).filter(Student.email == indata.email).first()

    if exist_std:
        raise HTTPException(status_code=400, detail="Student already Exists!")
    
    hashed_pswd = hash_password(indata.password)

    new_std = Student(
        name = indata.name,
        email = indata.email,
        password = hashed_pswd,
        university_id = cur_user["user_id"],
        degree = indata.degree,
        branch = indata.branch
    )
    db.add(new_std)
    db.commit()
    db.refresh(new_std)
    return{
        "msg" : "Student Registered!!",
        "std_id" : new_std.id
    }

@router.post("/login", status_code=200)
def login_student(indata: StudentLogin, db:Session = Depends(get_db)):

    std = db.query(Student).filter(Student.email == indata.email).first()

    if not std:
        raise HTTPException(status_code=404, detail="Student Not FOUND!")
    
    if not verify_password(indata.password, std.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = create_token(
        user_id= std.id,
        role= "student"
    )
    return{
        "msg" : "Student Login Successful!",
        "access_token" : token,
        "token_type" : "bearer"
    }

@router.get("/viewCertificates", status_code=200)
def get_certificates(db:Session = Depends(get_db), cur_user = Depends(get_cur_user)):

    if cur_user["role"] != "student":
        raise HTTPException(status_code=401, detail="Unauthorised!!")
    
    certis = db.query(Certificates).filter(Certificates.student_id == cur_user["user_id"]).all()

    if not certis:
        return {
            "msg" : "No certificates issued yet!!"
        }
    
    result = []

    for certi in certis:

        file_name = os.path.basename(certi.pdf_path)

        result.append({
            "certificate_id": certi.id,
            "degree": certi.degree,
            "branch": certi.branch,
            "certificate_hash": certi.certificate_hash,
            "block_index": certi.block_index,
            "pdf_url": f"/certificates/{file_name}"
        })

    return result
