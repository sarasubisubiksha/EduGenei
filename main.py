from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from services.ai_service import EduGenieAI, AIServiceError

load_dotenv()
BASE=Path(__file__).resolve().parent
app=FastAPI(title="EduGenie API",version="1.0.0")
app.mount("/static",StaticFiles(directory=BASE/"static"),name="static")
templates=Jinja2Templates(directory=BASE/"templates")
ai=EduGenieAI()

class TaskRequest(BaseModel):
    text:str=Field(...,min_length=2,max_length=20000)
    level:str=Field(default="Beginner",max_length=40)

@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(request=request,name="index.html",context={})

@app.get("/health")
async def health():
    return {"status":"ok","provider":"Google Gemini","api_key_configured":ai.configured}

async def process(task,body):
    if not ai.configured:
        raise HTTPException(503,"Set GEMINI_API_KEY in .env and restart the server.")
    try: return await ai.generate(task,body.text,body.level)
    except AIServiceError as e: raise HTTPException(502,str(e))

@app.post("/qa")
async def qa(body:TaskRequest): return await process("qa",body)
@app.post("/explain")
async def explain(body:TaskRequest): return await process("explain",body)
@app.post("/quiz")
async def quiz(body:TaskRequest): return await process("quiz",body)
@app.post("/summarize")
async def summarize(body:TaskRequest): return await process("summarize",body)
@app.post("/learn/recommendations")
async def recommend(body:TaskRequest): return await process("recommend",body)
