from fastapi import FastAPI
from pydantic import BaseModel
from chat import chatbot
from fastapi import FastAPI

from k8s import (
    get_pods,
    get_deployments,
    get_services,
    get_events,
    get_nodes,
    get_namespaces
)

app = FastAPI(title="OpenShift ChatBot")


@app.get("/")
def home():
    return {"message": "Welcome to OpenShift ChatBot"}


@app.get("/health")
def health():
    return {"status": "Healthy"}


@app.get("/pods")
def pods():
    return get_pods()


@app.get("/deployments")
def deployments():
    return get_deployments()


@app.get("/services")
def services():
    return get_services()


@app.get("/events")
def events():
    return get_events()


@app.get("/nodes")
def nodes():
    return get_nodes()


@app.get("/namespaces")
def namespaces():
    return get_namespaces()
