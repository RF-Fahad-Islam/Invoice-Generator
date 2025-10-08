from fastapi import FastAPI,Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from docxtpl import DocxTemplate
from datetime import datetime
from io import BytesIO

def generateInvoice(datas:dict):
    template = os.path.join(FILE_DIRECTORY, "invoice_template.docx")
    doc = DocxTemplate(template)
    doc.render(datas)
    fileio = BytesIO()
    doc.save(fileio)
    fileio.seek(0)
    return fileio
    
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
    file_io = generateInvoice(invoice.model_dump())
    filename = f"Invoice-{datetime.now().strftime('%d_%m_%Y %H-%M-%S')}.docx"
    return StreamingResponse(
        file_io,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}","filename": filename}
    )
