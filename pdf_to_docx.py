from pdf2docx import Converter
import os

def convert_pdf_to_docx(pdf_path, output_dir):
    output_path = os.path.join(output_dir, os.path.basename(pdf_path).replace(".pdf", ".docx"))
    cv = Converter(pdf_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    return {"converted": True, "output_file": output_path}