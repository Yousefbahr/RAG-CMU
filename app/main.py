from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from app.core.llm import get_response

# Pydantic model for input
class ChatRequest(BaseModel):
    message: str

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

# Mount static folder (for JS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Use Jinja2 for HTML templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    user_message = chat.message
    # Replace this with your actual chatbot logic

    response = get_response(user_message)
    #response = f"Echo : {user_message}"

    return JSONResponse({"response": response})
