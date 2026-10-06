from sqlalchemy import Column, Integer, String,Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database.dbase import Base


class University(Base):

    __tablename__ = "universities"

    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, unique= True)
    email = Column(String, unique=True)
    password = Column(String)
    #i.e two way updation where university is an attribute in the students table
    students = relationship("Student", back_populates="university")


class Student(Base):
    
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    university_id = Column(Integer, ForeignKey("universities.id"))
    university = relationship("University", back_populates= "students")

    degree = Column(String, nullable=False)
    branch = Column(String, nullable=False)

class Employer(Base):

    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique= True)
    password = Column(String)

class Certificates(Base):

    __tablename__ = "certificates"

    id = Column(Integer, primary_key= True, index= True)
    student_id = Column(Integer, ForeignKey("students.id"))
    university_id = Column(Integer, ForeignKey("universities.id"))

    degree = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    cgpa = Column(Float)

    pdf_path = Column(String)
    certificate_hash = Column(String)
    block_index = Column(Integer)

    # __table_args__ = (
    #     UniqueConstraint("student_id","degree","branch", name="unique_student_degree_branch"),
    # )
    