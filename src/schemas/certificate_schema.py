from pydantic import BaseModel

class IssueCertificate(BaseModel):

    student_id: int
    year: int
    cgpa: float

class CertificateResponse(BaseModel):

    id: int
    student_id: int
    certificate_hash: str
    block_index: int

    class Config:
        from_attributes = True