from pydantic import BaseModel, EmailStr

class EmployerRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class EmployerLogin(BaseModel):
    email: EmailStr
    password: str

