import requests

OLLAMA_URL = "http://ollama:11434"
MODEL = "llama3.2:1b"


def ask_gpt(question: str):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": question,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]
