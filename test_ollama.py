from ollama import chat

MODEL = "agent-local"

response = chat(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "Tu es un assistant IA. Réponds en français."
        },
        {
            "role": "user",
            "content": "Explique en 3 phrases ce qu'est un agent IA."
        }
    ]
)

print(response.message.content)