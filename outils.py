from pathlib import Path
from datetime import datetime 

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