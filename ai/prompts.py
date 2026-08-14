"""
Templates de prompts envoyés à l'API Groq.
Garder les prompts courts, contraints, et orientés "sortie utilisable directement".
"""

SYSTEM_PROMPT = (
    "Tu es l'assistant IA de ELYON, une plateforme qui aide les professionnels "
    "(développeurs, freelances, étudiants, designers) à générer un CV "
    "professionnel. Tu écris en français, de façon concise, professionnelle et "
    "sans emphase excessive. Tu ne dépasses jamais la longueur demandée."
)


def bio_generate_prompt(profession, skills, experience_years, tone="professionnel"):
    return (
        f"Rédige une bio professionnelle de 3 à 4 phrases (max 80 mots) pour "
        f"l'en-tête d'un CV. Métier : {profession}. Compétences clés : {skills}. "
        f"Expérience : {experience_years}. Ton : {tone}. "
        f"Réponds uniquement avec le texte de la bio, sans guillemets ni titre."
    )


def bio_improve_prompt(raw_text):
    return (
        "Voici un texte de présentation écrit par un utilisateur. Réécris-le pour "
        "le rendre plus professionnel, clair et impactant, en gardant le même sens "
        "et à peu près la même longueur. Réponds uniquement avec le texte réécrit.\n\n"
        f"Texte original :\n{raw_text}"
    )


def skill_suggestions_prompt(profession, existing_skills):
    return (
        f"Un utilisateur a pour métier « {profession} » et possède déjà les "
        f"compétences suivantes : {existing_skills or 'aucune'}. "
        f"Propose 8 compétences supplémentaires pertinentes, sous forme de liste "
        f"séparée par des virgules, sans numérotation ni explication."
    )


def profile_analysis_prompt(profile_summary):
    return (
        "Voici un résumé JSON d'un profil ELYON. Analyse-le et fournis : "
        "1) les 2-3 points forts, 2) les 2-3 éléments manquants ou à améliorer "
        "pour un CV professionnel. Réponds en 5 lignes maximum, format liste à puces.\n\n"
        f"{profile_summary}"
    )


def assistant_prompt(user_question, context_summary=""):
    context_part = f"\nContexte du profil de l'utilisateur : {context_summary}" if context_summary else ""
    return (
        f"Question de l'utilisateur concernant l'amélioration de son profil ou "
        f"de son CV : {user_question}{context_part}\n"
        f"Réponds de façon concrète et actionnable, en 5 phrases maximum."
    )
