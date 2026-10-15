from ollama import chat

MODEL = "agent-local"

# Outil accessible à l'agent
def calculer_tva(prix_ht: float, taux: float = 20) -> float:
    """Calcule le prix TTC à partir du prix HT et du taux de TVA."""
    return round(prix_ht * (1 + taux / 100), 2)


messages = [
    {
        "role": "system",
        "content": (
            "Tu es un assistant IA français. "
            "Utilise les outils lorsque cela est pertinent. "
            "Réponds toujours en français."
        )
    }
]

print("Agent IA prêt. Tape 'quitter' pour arrêter.")

while True:
    question = input("\nVous : ").strip()

    if question.lower() == "quitter":
        break

    messages.append({"role": "user", "content": question})

    for _ in range(5):
        response = chat(
            model=MODEL,
            messages=messages,
            tools=[calculer_tva]
        )

        messages.append(response.message)

        if not response.message.tool_calls:
            print("\nAgent :", response.message.content)
            break

        for call in response.message.tool_calls:
            if call.function.name == "calculer_tva":
                try:
                    resultat = calculer_tva(
                        **call.function.arguments
                    )
                except (TypeError, ValueError) as e:
                    resultat = f"Erreur : {e}"
            else:
                resultat = "Outil non autorisé"

            messages.append({
                "role": "tool",
                "tool_name": call.function.name,
                "content": str(resultat)
            })
    else:
        print("Limite d'appels d'outils atteinte.")