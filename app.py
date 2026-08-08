from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chat import chatbot

app = FastAPI(title="OCP Cluster Assistant")


class ChatRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r") as file:
        return file.read()


@app.post("/chat")
def chat(request: ChatRequest):
    return chatbot(request.question)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "OCP Cluster Assistant"
    }
