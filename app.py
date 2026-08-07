from fastapi import FastAPI
from k8s import get_pods

app = FastAPI(title="OpenShift ChatBot")

@app.get("/")
def root():
    return {
        "message": "Welcome to OpenShift ChatBot"
    }

@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }

@app.get("/pods")
def pods():
    return get_pods()
