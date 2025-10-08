from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from docxtpl import DocxTemplate
from datetime import datetime
import tempfile
from typing import Annotated

def generateInvoice(datas:dict):
    template = os.path.join(FILE_DIRECTORY, "invoice_template.docx")
    doc = DocxTemplate(template)
    doc.render(datas)
    # Create a temporary file to save the generated DOCX
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        file_name = f"Invoice-{datetime.now().strftime('%d_%m_%Y %H-%M-%S')}.docx"
        doc.save(os.path.join(FILE_DIRECTORY_2,file_name))

    return file_name
    
class Item(BaseModel):
    item_name: str
    item_desc:str
    item_qty:int
    item_price:float
    line_total:float

class Invoice(BaseModel):
    company_name:str
    bill_to:str
    phone:int
    items: list[Item]
    subtotal: float
    salestax:int
    total: float
    
    
app = FastAPI()
FILE_DIRECTORY = "files"
FILE_DIRECTORY_2 = "genfiles"
app.add_middleware(CORSMiddleware,   allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="template")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": "1"}
    )
@app.post("/invoice")
async def invoice_generator(invoice:Invoice):
    file_name = generateInvoice(invoice.model_dump())
    return {"file_name":file_name}



@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(FILE_DIRECTORY_2, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found!"}

    return FileResponse(
        file_path,
        media_type="application/octet-stream"  # Generic binary data
    )

def removejunk(file_name):
    os.remove(os.path.join(FILE_DIRECTORY_2,file_name))
