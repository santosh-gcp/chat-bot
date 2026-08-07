from fastapi import FastAPI
from k8s import get_pods

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to OCP Chatbot"}

@app.get("/pods")
def pods():
    return get_pods("santoshvih-dev")
