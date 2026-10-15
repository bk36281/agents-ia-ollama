import json
from pathlib import Path

# Fichier mémoire persistante

FICHIER = Path(__file__).with_name("memoire.json")

def charger_memoire():
    if FICHIER.exists():
        with FICHIER.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_memoire(messages):
    with FICHIER.open("w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)