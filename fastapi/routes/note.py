from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request,Form
from fastapi.responses import HTMLResponse
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity,notesEntity
from typing import Annotated

note =APIRouter()
templates = Jinja2Templates(directory="templates")



@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs= await conn.notes.notes.find({})
    newDocs=[]
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "title" : doc["title"],
            "desc" : doc["desc"],
            "important": doc["important"],
        })

    return templates.TemplateResponse( "index.html",{"request":request,"newDocs" : newDocs})

@note.post("/")
async def read_item(request: Request):
    form= await request.form()
    formDict= dict(form)
    formDict["imortant"]=True if formDict["imortant"]== "on" else False
    note= conn.notes.notes.insert_one(formDict)
    return {"success": True}
