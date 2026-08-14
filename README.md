# ELYON Portfolio

Plateforme SaaS permettant à un utilisateur de créer une identité professionnelle
numérique complète en quelques minutes : profil, portfolio, CV automatique,
QR Code, statistiques, et assistant IA (Groq).

URL publique type : `http://127.0.0.1:8000/u/elvis/`

## Fonctionnalités incluses (MVP)

- **Comptes** : inscription, connexion, déconnexion
- **Profil professionnel** : photo, nom, métier, localisation, bio, dispo, coordonnées
- **Portfolio** : projets (titre, description, image, technos, GitHub, démo, vedette)
- **Réseaux sociaux** : GitHub, LinkedIn, Facebook, Instagram, X, YouTube, TikTok, site perso
- **Compétences / Expériences / Formations**
- **Thèmes** : minimal, developer, corporate, creative, glass, dark (couleurs personnalisables)
- **Professional Score** : score /100 calculé automatiquement + conseils d'amélioration
- **Analytics** : vues du profil, visiteurs uniques, clics par lien, projets les plus vus, courbe 14 jours
- **CV automatique** : génération PDF (ReportLab) à partir des données du profil
- **QR Code** : généré automatiquement vers l'URL publique du profil
- **Page publique** : `/u/<username>/`, responsive, avec SEO (title, description, Open Graph)
- **Assistant IA (Groq)** : génération/amélioration de bio, description de projet,
  suggestions de compétences, analyse de profil, assistant conversationnel
- **Plan Free / Pro / Business** (structure de base — limite de 3 projets en Free)
- **Admin Django** configuré pour tous les modèles

## Stack technique

- Backend : Python, Django
- Base de données : SQLite (dev) — PostgreSQL recommandé en production
- Frontend : Bootstrap 5 (CDN) + CSS custom
- IA : Groq API (`ai/services.py`)
- PDF : ReportLab
- QR Code : bibliothèque `qrcode`

## Installation

```bash
# 1. Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# → édite .env et ajoute ta clé GROQ_API_KEY si tu veux utiliser l'IA

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un compte administrateur
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

Rends-toi sur `http://127.0.0.1:8000/` pour voir la landing page,
`http://127.0.0.1:8000/admin/` pour l'admin Django.

## Architecture

```
elyon/
├── manage.py
├── requirements.txt
├── .env.example
├── config/            # settings, urls, wsgi
├── accounts/          # inscription / connexion
├── profiles/          # profil, thèmes, réseaux sociaux, page publique, QR code
├── projects/          # portfolio / projets
├── analytics/         # vues, clics, téléchargements CV
├── ai/                # intégration Groq (services.py, prompts.py, views.py)
├── cvgen/             # génération de CV PDF
├── templates/          # tous les templates HTML
└── static/             # CSS custom
```

## Configurer la clé Groq

1. Crée un compte sur https://console.groq.com
2. Génère une clé API
3. Ajoute-la dans `.env` :
   ```
   GROQ_API_KEY=ta_cle_ici
   ```

Sans clé configurée, les fonctionnalités IA du dashboard renverront un message
d'erreur explicite mais le reste de l'application fonctionne normalement.

## Prochaines étapes suggérées (Phase 4 / 5 du cahier des charges)

- Système d'abonnement / paiement (Pro, Business)
- Domaine personnalisé par utilisateur
- Comptes Business multi-profils
- API publique
- Déploiement production (PostgreSQL, Gunicorn/Nginx, stockage médias sur S3)
- Tests automatisés
- Thèmes publics supplémentaires (corporate, creative, glass déjà prévus dans les choix
  du modèle — templates HTML à compléter sur le même modèle que `profiles/public/minimal.html`)

---

Généré comme base de projet Django complète et fonctionnelle, prête à être étendue.
