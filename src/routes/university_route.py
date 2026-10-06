from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from src.database.dbase import get_db
from src.models.all_models import University, Student
from src.schemas.university_schema import UniversityRegister, UniversityLogin
from src.utils.password_handler import hash_password, verify_password
from src.utils.jwt_rbac_handler import create_token, verify_token
from src.utils.auth_dependency import get_cur_user

router = APIRouter(
    prefix= "/university",
    tags=["University"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_university(indata: UniversityRegister, db: Session= Depends(get_db)):

    existing_uni = db.query(University).filter(University.email == indata.email).first()

    if existing_uni:
        raise HTTPException(status_code=400, detail="Already Registered!!")
    
    hashed_psw = hash_password(indata.password)

    new_uni = University(
        name = indata.name,
        email = indata.email,
        password = hashed_psw
    )
    db.add(new_uni)
    db.commit()
    db.refresh(new_uni)

    return {
        "msg" : "University registered Successfully!",
        "uni_id" : new_uni.id
    }

@router.post("/login", status_code=200)
def login_university(indata: UniversityLogin, db: Session = Depends(get_db)):

    uni = db.query(University).filter(University.email == indata.email).first()

    if not uni:
        raise HTTPException(status_code=404, detail="University Not registered yet!!")
    if not verify_password(indata.password, uni.password):
        raise HTTPException(status_code=401, detail="Unauthorised Access!!")
    
    token = create_token(
        user_id= uni.id,
        role= "university"
    )
    return{
        "msg" : "Login Successful!",
        "access_token" : token,
        "token_type" : "bearer"
    }

# @router.get("/protect_auth")
# def testing(cur_user = Depends(get_cur_user)):
#     return cur_user

# @router.get("/getAll")
# def get_all_universities(db:Session = Depends(get_db)):
    
#     std_list = db.query(University).all()
#     return std_list

@router.get("/allStudents", status_code=200)
def get_all_students(db: Session = Depends(get_db), cur_user = Depends(get_cur_user)):

    if cur_user["role"] != "university":
        raise HTTPException(status_code=403, detail="Only University allowed!")

    students = db.query(Student).filter(Student.university_id == cur_user["user_id"]).all()

    if not students:
        return {"msg": "No students found"}

    result = []
    for student in students:
        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "degree": student.degree,
            "branch": student.branch
        })

    return result