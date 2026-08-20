import os
import requests


QWEN_API_URL = os.getenv(
    "QWEN_API_URL",
    "https://chatting-acetone-lapped.ngrok-free.dev/generate"
)


def generate_answer(prompt):

    response = requests.post(
        QWEN_API_URL,
        json={
            "prompt": prompt
        },
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data["answer"]