from fpdf import FPDF
from src.models.all_models import Student
from src.schemas.certificate_schema import IssueCertificate
from datetime import date
import os

async def make_pdf(student: Student, indata: IssueCertificate, uni_name, serial_no):

    os.makedirs("certificates", exist_ok=True)

    # Initialize PDF (Landscape A4)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Borders
    pdf.set_draw_color(184, 134, 11) # Gold
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 277, 190) 
    pdf.set_draw_color(40, 45, 52) # Dark Slate
    pdf.set_line_width(0.2)
    pdf.rect(12, 12, 273, 186)

    # Serial Number (Top Right)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(220, 15)
    pdf.cell(50, 10, f"Serial No: {serial_no}", 0, 1, 'R')

    # University Name
    pdf.set_text_color(40, 45, 52)
    pdf.set_font('Times', 'B', 32)
    pdf.set_y(25)
    pdf.cell(0, 15, uni_name, 0, 1, 'C')

    # Phrases and Layout based on your sample
    pdf.ln(10)
    pdf.set_font('Times', 'I', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'this is to certify that', 0, 1, 'C')

    pdf.set_font('Times', 'B', 28)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, student.degree, 0, 1, 'C')

    pdf.set_font('Times', 'I', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'in', 0, 1, 'C')

    pdf.set_font('Times', 'B', 22)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, student.branch, 0, 1, 'C')

    pdf.set_font('Times', 'I', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'on', 0, 1, 'C')

    pdf.set_font('Times', 'B', 30)
    pdf.set_text_color(184, 134, 11) # Gold accent for name
    pdf.cell(0, 15, student.name.upper(), 0, 1, 'C')

    pdf.set_font('Times', 'I', 15)
    pdf.set_text_color(80, 80, 80)
    pdf.ln(5)
    pdf.cell(0, 8, 'on having successfully completed the prescribed requirements', 0, 1, 'C')
    pdf.set_font('Times', 'B', 15)
    pdf.cell(0, 8, f'with CGPA of {indata.cgpa} in the academic year {indata.year}', 0, 1, 'C')

    # Digital Signatures
    pdf.ln(20)
    curr_y = pdf.get_y()

    # Signature Styling
    pdf.set_font('Courier', 'BI', 11)
    pdf.set_text_color(30, 80, 150) 

    # Principal
    pdf.set_xy(200, curr_y-10)
    pdf.multi_cell(100, 5, f"Auth ID: PRN-KK901\nDate: {date.today()}", 0, 'C')

    file_name = f"{student.name}.pdf"
    file_path = f"certificates/{file_name}"

    pdf.output(file_path)

    return file_path