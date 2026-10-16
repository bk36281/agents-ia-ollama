
from ollama import chat
from outils import OUTILS
from memoire import charger_memoire, sauvegarder_memoire

MODEL = "agent-local"
MAX_CYCLES = 5

SYSTEM = {
    "role": "system",
    "content": (
        "Tu es un agent IA local utilisant Ollama. "
        "Réponds toujours en français. "
        "Utilise les outils lorsque c'est nécessaire. "
        "Utilise uniquement les informations pertinentes "
        "de l'historique pour répondre à la question actuelle. "
        "Ne mentionne pas d'anciens projets, personnages ou sujets "
        "s'ils ne sont pas directement liés à la demande. "
        "Si une information n'est pas disponible, indique-le "
        "plutôt que de l'inventer. "
        "Privilégie les réponses concises et précises."
    )
}


def executer_agent(messages):
    """Exécute la boucle agentique."""

    for _ in range(MAX_CYCLES):

        response = chat(
            model=MODEL,
            messages=messages,
            tools=list(OUTILS.values())
        )

        # Conserver la réponse du modèle
        messages.append(
            response.message.model_dump(exclude_none=True)
        )

        # Aucun outil demandé : réponse finale
        if not response.message.tool_calls:
            return response.message.content

        # Exécuter les outils demandés
        for call in response.message.tool_calls:

            nom = call.function.name
            arguments = call.function.arguments

            print(f"[OUTIL] {nom}({arguments})")

            if nom not in OUTILS:
                resultat = "Outil non autorisé"
            else:
                try:
                    resultat = OUTILS[nom](**arguments)
                except Exception as e:
                    resultat = f"Erreur : {e}"

            # Transmettre le résultat à Qwen
            messages.append({
                "role": "tool",
                "tool_name": nom,
                "content": str(resultat)
            })

    return "Limite de cycles atteinte."


def main():

    # Initialisation de l'agent 
    messages = [SYSTEM] + charger_memoire()

    print("=== AGENT IA LOCAL ===")
    print("Modèle :", MODEL)
    print("Mémoire et outils activés.")
    print("Tape 'quitter' pour arrêter.")

    while True:

        question = input("\nVous : ").strip()

        if question.lower() == "quitter":
            break

        if not question:
            continue

        messages.append({
            "role": "user",
            "content": question
        })

        try:
            reponse = executer_agent(messages)
            print("\nAgent :", reponse)

        except Exception as e:
            print(f"\nErreur : {e}")
            # Ne pas sauvegarder une conversation incomplète
            messages = [SYSTEM] + charger_memoire()
            continue

        # Sauvegarder après chaque demande traitée
        sauvegarder_memoire(messages[1:])

    print("Agent arrêté.")


if __name__ == "__main__":
    main()
