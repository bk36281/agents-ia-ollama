from pathlib import Path
from datetime import datetime 
from ollama import chat

MODEL = "agent-local"

#Agent multi-outils

# Dossier dans lequel l'agent peut lire des fichiers
DOCUMENTS = Path(__file__).parent / "documents"

# OUTIL 1 : Calculatrice
def calculer(a: float, b: float, operation: str) -> float:
    """Effectue une opération : addition, soustraction,
    multiplication ou division."""

    if operation == "addition":
        return a + b
    if operation == "soustraction":
        return a - b
    if operation == "multiplication":
        return a * b
    if operation == "division":
        if b == 0:
            raise ValueError("Division par zéro")
        return a / b

    raise ValueError("Opération inconnue")


# OUTIL 2 : Date et heure
def date_heure() -> str:
    """Retourne la date et l'heure locales du PC."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# OUTIL 3 : Lecture de fichier
def lire_fichier(nom: str) -> str:
    """Lit un fichier TXT du dossier documents."""

    dossier = DOCUMENTS.resolve()
    fichier = (dossier / nom).resolve()

    if not fichier.is_relative_to(dossier):
        return "Accès interdit : fichier hors du dossier documents."

    if fichier.suffix.lower() != ".txt":
        return "Seuls les fichiers TXT sont autorisés."

    if not fichier.is_file():
        return "Fichier introuvable."

    if fichier.stat().st_size > 100_000:
        return "Fichier trop volumineux."

    return fichier.read_text(encoding="utf-8")

# Registre des outils autorisés
OUTILS = {
    "calculer": calculer,
    "date_heure": date_heure, 
    "lire_fichier": lire_fichier
}

# Historique de conversation
messages = [
    {
        "role": "system",
        "content": (
            "Tu es un agent IA local spécialisé en Python. "
            "Tu réponds toujours en français. "
            "Tu disposes de trois outils : "
            "calculer, date_heure et lire_fichier. "
            "Pour toute question concernant la date ou l'heure actuelle, "
            "tu dois utiliser date_heure. "
            "Pour les calculs, utilise calculer. "
            "Pour lire un document, utilise lire_fichier. "
            "Ne prétends pas ne pas avoir accès à une information "
            "avant d'avoir vérifié si un outil permet de l'obtenir."
        )
    }
]

print("Agent multi-outils opérationnel et prêt à aider")
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

    for _ in range(5):

        response = chat(
            model=MODEL,
            messages=messages,
            tools=list(OUTILS.values())
        )

        messages.append(response.message)

        if not response.message.tool_calls:
            print("\nAgent :", response.message.content)
            break

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

            messages.append({
                "role": "tool",
                "tool_name": nom,
                "content": str(resultat)
            })

    else:
        print("Limite de cycles atteinte.")
