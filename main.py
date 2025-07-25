from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from converters import pdf_to_docx, docx_to_pdf, pdf_to_txt, txt_to_pdf, image_converter
import shutil
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/convert")
async def convert(file: UploadFile = File(...), target_format: str = "docx"):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ext = file.filename.split(".")[-1].lower()

    if ext == "pdf" and target_format == "docx":
        result = pdf_to_docx.convert_pdf_to_docx(file_path, OUTPUT_DIR)
    elif ext == "docx" and target_format == "pdf":
        result = docx_to_pdf.convert_docx_to_pdf(file_path, OUTPUT_DIR)
    elif ext == "pdf" and target_format == "txt":
        result = pdf_to_txt.convert_pdf_to_txt(file_path, OUTPUT_DIR)
    elif ext == "txt" and target_format == "pdf":
        result = txt_to_pdf.convert_txt_to_pdf(file_path, OUTPUT_DIR)
    elif ext in ["png", "jpg", "jpeg"]:
        result = image_converter.convert_image(file_path, target_format, OUTPUT_DIR)
    else:
        return {"error": "Unsupported format"}

    return result