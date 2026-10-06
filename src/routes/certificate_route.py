from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import hashlib

from src.services.create_pdf import make_pdf

from src.database.dbase import get_db
from src.models.all_models import Student, Certificates
from src.schemas.certificate_schema import IssueCertificate
from src.utils.auth_dependency import get_cur_user
from src.BlockChainLocal.blockchain_instance import blockchain  #this creates instance for once and reuses it always.... otherwise everytime new chain gets created!!
from src.BlockChainLocal.block import Block_bluePrint

router = APIRouter(
    prefix="/certificate",
    tags=["Certificate"]
)

@router.post("/issue", status_code=201)
async def issue_certificate(indata: IssueCertificate, db:Session = Depends(get_db), cur_user = Depends(get_cur_user)):

    if cur_user["role"] != "university":
        raise HTTPException(status_code=403, detail="Only University can Issue!!")
    
    std_now = db.query(Student).filter(Student.id == indata.student_id).first()
    if not std_now:
        raise HTTPException(status_code=404, detail="Student not FOUND!")
    
    degree_std = std_now.degree
    branch_std = std_now.branch
    
    exist_cert = db.query(Certificates).filter(
        Certificates.student_id == std_now.id,
        Certificates.degree == degree_std,
        Certificates.branch == branch_std
    ).first()

    if exist_cert:
        raise HTTPException(status_code= 400, detail="Already exists!!")
    
    #we first store certificate in database, then obtain the cert_id from db...
    cert_from_db = Certificates(
        student_id = std_now.id,
        university_id = cur_user["user_id"],
        degree = degree_std,
        branch = branch_std,
        cgpa = indata.cgpa
    )
    db.add(cert_from_db)
    db.commit()
    db.refresh(cert_from_db)
    cert_id = cert_from_db.id   #from database

    uni_name = std_now.university.name
    serial_no = f"CERT-{cur_user["user_id"]:03d}-{cert_id:05d}"

    file_path = await make_pdf(std_now, indata, uni_name, serial_no)

    with open(file_path, "rb") as f:
        file_bytes = f.read()
        cert_hash = hashlib.sha256(file_bytes).hexdigest()

    #add into BlockChain... and get block_index then update into database
    blockchain.add_tranxn(
        issuer= cur_user["user_id"],
        receiver= std_now.name,
        certi_id=cert_id,
        certi_hash= cert_hash
    )
    block_index = blockchain.insert_block(str(cur_user["user_id"]))

    cert_from_db.pdf_path = file_path
    cert_from_db.certificate_hash = cert_hash
    cert_from_db.block_index = block_index
    db.commit()
    db.refresh(cert_from_db)

    return{
        "msg" : "Certificate issued !!",
        "certificate_id" : cert_id,
        "certificate_hash" : cert_hash,
        "block_index" : block_index
    }

@router.get("/blockchain")
def view_blockchain():

    block : Block_bluePrint

    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.to_dict())

    return chain_data