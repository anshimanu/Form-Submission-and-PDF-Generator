from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import db
from bson import ObjectId
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from docxtpl import DocxTemplate
import os
import subprocess
import uuid
import logging
import traceback

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

#Pydantic Model
class FormData(BaseModel):
    FullName: str
    Email: str
    Mobile: str
    Company: str
    Role: str
    Address: str
    City: str
    State: str
    PinCode: str
    Date: str
    Remarks: str

#Submission Insert Endpoint
@app.post("/submit")
async def submit_form(data: FormData):
    result = await db["submissions"].insert_one(data.dict())
    return {"inserted_id": str(result.inserted_id)}

#Get All Submissions Endpoint
@app.get("/submissions")
async def get_submissions():
    submissions = []
    cursor = db["submissions"].find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        submissions.append(doc)
    return submissions

# @app.post("/generate-pdf")
# async def generate_pdf(data: FormData):

#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     template_path = os.path.join(current_dir, "template.docx")
#     libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

#     filled_docx_path = None

#     try:
#         doc = DocxTemplate(template_path)
#         doc.render(data.dict())

#         filled_docx_path = os.path.join(current_dir, "filled_template.docx")
#         doc.save(filled_docx_path)

#         if filled_docx_path is None:
#             raise Exception("Filled DOCX path was not set.")

#         result = subprocess.run([
#             libreoffice_path,
#             "--headless",
#             "--convert-to", "pdf:writer_pdf_Export:ExportFormFields=false",
#             "--outdir", current_dir,
#             filled_docx_path
#         ], capture_output=True, text=True, check = True)
#         logging.info("LibreOffice stdout: " + result.stdout)
#         logging.error("LibreOffice stderr: " + result.stderr)

#         if result.returncode != 0:
#             raise Exception("LibreOffice conversion failed")

#         # subprocess.run([
#         #     libreoffice_path,
#         #     "--headless",
#         #     "--convert-to", "pdf",
#         #     "--outdir", ".",
#         #     filled_docx_path
#         # ], check=True)

#         # print("Current Working Directory:", os.getcwd())
#         # print("Template file absolute path:", template_path)

#         # doc = DocxTemplate(template_path)

#         # context = data.dict()
#         # doc.render(context)

#     except Exception as e:
#         logging.error("Error generating PDF:\n" + traceback.format_exc())
#         raise HTTPException(status_code=500, detail="Error while generating PDF")


@app.post("/generate-pdf")
async def generate_pdf(data: FormData):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "template.docx")
    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    filled_docx_path = os.path.join(current_dir, "filled_template.docx")
    try:
        doc = DocxTemplate(template_path)
        doc.render(data.dict())
        doc.save(filled_docx_path)

        result = subprocess.run([
            libreoffice_path,
            "--headless",
            "--convert-to", 'pdf:writer_pdf_Export:{"ExportFormFields":{"type":"boolean","value":"false"}}',
            "--outdir", current_dir,
            filled_docx_path
        ], capture_output=True, text=True, check=True)

        logging.info("LibreOffice stdout: " + result.stdout)
        logging.error("LibreOffice stderr: " + result.stderr)

        if result.returncode != 0:
            raise Exception("LibreOffice conversion failed")

        pdf_path = filled_docx_path.replace(".docx", ".pdf")

        if not (os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0):
            raise Exception("PDF file not created or empty")

        return FileResponse(pdf_path, media_type="application/pdf", filename="output.pdf")

    except Exception as e:
        logging.error("Error generating PDF:\n" + traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error while generating PDF")  