from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="OCP Chatbot",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to OCP Chatbot"
    }

@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }

@app.get("/version")
def version():
    return {
        "application": "OCP Chatbot",
        "version": "1.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
