import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_gpt(question: str):

    response = client.responses.create(
        model="gpt-5.5",
        input=question
    )

    return response.output_text
