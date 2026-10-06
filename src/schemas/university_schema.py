from pydantic import BaseModel, EmailStr

class UniversityRegister(BaseModel):

    name: str
    email: EmailStr
    password: str

class UniversityLogin(BaseModel):
    
    email: EmailStr
    password: str

class UniversityResponse(BaseModel):

    id: int
    name: str
    email: EmailStr

    #from_attributes required for SQLAlchemy Objects... when retrieving and responding to api request...
    class Config:
        from_attributes = True