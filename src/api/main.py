from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.BlockChainLocal.blockChain import BlockChain, Block_bluePrint
from src.database.dbase import engine, Base
# from models import all_models
from src.routes import university_route, student_route, certificate_route, employer_route

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title= "Certiveri Blockchain API",
    description= "Certificate Verification using Blockchain",
    version= "1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(university_route.router)
app.include_router(student_route.router)
app.include_router(certificate_route.router)
app.include_router(employer_route.router)

app.mount("/certificates", StaticFiles(directory="certificates"), name="certificates")

@app.get("/", status_code=200)
def root():
    return {
        "msg" : "Its on!!"
    }


