from ollama import chat
from memoire import charger_memoire, sauvegarder_memoire

MODEL = "agent-local"

SYSTEM = {
    "role": "system",
    "content": "Tu es un agent IA spécialisé en Python. Réponds en français."
}

messages = [SYSTEM] + charger_memoire()

print("Agent avec mémoire prêt !")
print("Tape 'quitter' pour arrêter.")

while True:
    question = input("\nVous : ").strip()

    if question.lower() == "quitter":
        break

    messages.append({
        "role": "user",
        "content": question
    })

    try:
        response = chat(
            model=MODEL,
            messages=messages
        )
    except Exception as e:
        messages.pop()
        print(f"Erreur Ollama : {e}")
        continue

    reponse = response.message.content or ""
    print("\nAgent :", reponse)

    messages.append({
        "role": "assistant",
        "content": reponse
    })

    sauvegarder_memoire(messages[1:])