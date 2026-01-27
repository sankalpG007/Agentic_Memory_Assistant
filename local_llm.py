# local_llm.py
import ollama

def generate_response(prompt):
    response = ollama.chat(
        model="tinyllama",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]
