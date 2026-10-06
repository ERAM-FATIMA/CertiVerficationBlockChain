from pydantic import BaseModel, EmailStr

class StudentRegister(BaseModel):
    name: str
    email: EmailStr
    password : str
    branch: str
    degree: str

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class StudentResponse(BaseModel):

    id:int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True