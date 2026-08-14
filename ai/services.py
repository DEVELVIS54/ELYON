"""
Service d'intégration Groq pour LinkBio/ELYON.

Architecture :
    Vue Django -> ai.services.call_groq() -> API Groq -> texte généré

La clé API est lue depuis settings.GROQ_API_KEY (chargée depuis .env).
Ne jamais committer de clé en dur dans ce fichier.
"""

import requests
from django.conf import settings

from .prompts import SYSTEM_PROMPT

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class AIServiceError(Exception):
    """Levée quand l'appel à Groq échoue ou que la clé API est absente."""
    pass


def call_groq(user_prompt, max_tokens=300, temperature=0.7):
    """
    Envoie un prompt à l'API Groq (format compatible OpenAI chat completions)
    et retourne le texte de la réponse.
    """
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise AIServiceError(
            "GROQ_API_KEY n'est pas configurée. Ajoute-la dans ton fichier .env."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AIServiceError(f"Erreur lors de l'appel à Groq : {exc}") from exc

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise AIServiceError(f"Réponse Groq inattendue : {data}") from exc


# --- Fonctions métier de haut niveau -----------------------------------

def generate_bio(profession, skills, experience_years, tone="professionnel"):
    from .prompts import bio_generate_prompt
    return call_groq(bio_generate_prompt(profession, skills, experience_years, tone))


def improve_bio(raw_text):
    from .prompts import bio_improve_prompt
    return call_groq(bio_improve_prompt(raw_text))


def suggest_skills(profession, existing_skills):
    from .prompts import skill_suggestions_prompt
    result = call_groq(skill_suggestions_prompt(profession, existing_skills))
    return [s.strip() for s in result.split(',') if s.strip()]


def analyze_profile(profile_summary):
    from .prompts import profile_analysis_prompt
    return call_groq(profile_analysis_prompt(profile_summary))


def ask_assistant(user_question, context_summary=""):
    from .prompts import assistant_prompt
    return call_groq(assistant_prompt(user_question, context_summary), max_tokens=400)
