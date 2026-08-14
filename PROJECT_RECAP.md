# ELYON — Récapitulatif du projet

> Document à coller (ou joindre le dossier `elyon/` en entier) au début d'une
> nouvelle conversation pour reprendre le projet là où il en est.

## ⚠️ PIVOT MAJEUR (dernière session) — lire en premier

Le projet s'appelait "ELYON Portfolio" et proposait à la fois un portfolio
public (page `elyon.com/u/<username>`, 10 thèmes visuels, CRUD de projets)
ET un CV PDF. **Le portfolio a été entièrement retiré.** Le site est
désormais **exclusivement dédié à la génération de CV par IA**.

Décisions actées avec l'utilisateur (DEVELVIS) :
1. Plus de portfolio, plus de page publique par utilisateur, plus de QR code
   (son seul usage était de pointer vers la page publique).
2. Le site devient : **connexion → remplir ses informations → choisir un
   thème → générer/télécharger le CV**. Rien de plus.
3. Un **catalogue de thèmes de CV** va remplacer l'ancien catalogue de
   thèmes portfolio. Différence importante : **l'utilisateur remplira
   lui-même ce catalogue avec des images qu'il choisit** (pas de génération
   d'images par Claude).
4. Le principe de génération : l'utilisateur choisit un thème (image de
   référence) → remplit ses informations → **l'IA génère le CV en
   s'inspirant du thème choisi (couleur, design, mise en page)**.
5. Approche technique validée pour ce pipeline (cohérente avec ce qui avait
   été discuté pour l'ex-portfolio) : image de référence → IA vision
   analyse l'image → "fiche de style" structurée (palette, typographie,
   archétype de mise en page) → moteur de rendu **paramétrable** qui génère
   le PDF final. Pas de génération de code/design brut à chaque fois par
   l'IA (jugé trop peu fiable pour un rendu "très professionnel").

**Ce chantier (catalogue de thèmes CV + pipeline IA vision) n'est PAS encore
implémenté.** Seul le retrait du portfolio et le nettoyage du code sont
faits. Voir section 9 pour le détail de ce qui reste à construire.

## 1. Vision du projet (mise à jour)

ELYON est une plateforme qui permet à un utilisateur (développeur,
freelance, étudiant, designer, consultant) de générer en quelques minutes
un **CV professionnel**, avec une forte implication de l'IA dans la
rédaction et (à terme) la mise en page.

Positionnement : *« L'utilisateur fournit les informations, ELYON génère un
CV professionnel, optimisé par l'IA. »*

Le site n'a plus de page publique — tout se passe derrière connexion,
jusqu'au téléchargement du PDF.

## 2. Stack technique

- **Backend** : Python / Django 6.1
- **Base de données** : SQLite (dev), PostgreSQL recommandé en production
- **Frontend** : Bootstrap 5 (CDN) + CSS custom (`static/css/elyon.css`)
- **IA texte** : API Groq (`ai/services.py`, format compatible OpenAI chat completions)
- **PDF** : ReportLab (génération de CV) — un seul layout pour l'instant,
  voir section 9 pour l'évolution vers plusieurs thèmes
- **Secrets** : `python-dotenv` + fichier `.env`

Retiré cette session : `qrcode` (plus d'usage, son seul rôle était de
pointer vers la page publique disparue).

## 3. Architecture (apps Django) — mise à jour

```
elyon/
├── accounts/    → inscription, connexion, déconnexion
├── profiles/    → profil, réseaux sociaux, compétences, expériences, formations, dashboard
├── ai/          → intégration Groq (services.py, prompts.py, views.py)
├── cvgen/       → génération de CV PDF (generate + download, propriétaire uniquement)
├── templates/   → tous les templates HTML (voir section 6)
└── static/      → CSS custom (plus d'images d'aperçu de thèmes — supprimées)
```

**Apps supprimées cette session** : `projects` (CRUD projets/portfolio),
`analytics` (tracking de vues/clics sur la page publique — n'a plus de sens
sans page publique).

## 4. Modèle de données (mis à jour)

- `User` (Django auth) —1—1→ `Profile` (photo, bio, couleur d'accent, plan)
- `Profile` —1—N→ `SocialLink`, `Skill`, `Experience`, `Education`
- `User` —1—N→ `AIRequest` (historique des appels IA, app `ai`)

**Retiré du modèle `Profile`** : `theme` (THEME_CHOICES, 10 thèmes
portfolio), `secondary_color`, `seo_title`, `seo_description`, `og_image`,
`qr_code`. Le champ `primary_color` est conservé — c'est la couleur
d'accent utilisée dans le CV PDF généré (`cvgen/services.py`).

**Modèles supprimés** : `Project` (app `projects`), `ProfileView`,
`LinkClick`, `CVDownload` (app `analytics`).

### Nouveau calcul du Professional Score (/100)

L'ancien score comptait les projets (15 pts). Rebalancé sur des critères
100% pertinents pour un CV :
- Identité complète (nom + métier + bio) : 15 pts
- Photo : 10 pts
- Lien GitHub : 10 pts · Lien LinkedIn : 10 pts
- Compétences renseignées : 15 pts
- Expérience renseignée : 15 pts
- Formation renseignée : 15 pts (nouveau — n'était pas noté avant)
- CV généré : 10 pts

## 5. Fonctionnalités actuelles (testées de bout en bout via Django Test Client)

- Authentification complète (inscription / connexion / déconnexion)
- Profil : photo, nom, métier, localisation, bio, dispo, coordonnées
- Réseaux sociaux (GitHub, LinkedIn, Facebook, Instagram, X, YouTube, TikTok, site perso)
- Compétences / Expériences / Formations (CRUD complet)
- Professional Score (/100) calculé automatiquement + conseils d'amélioration
- CV PDF généré automatiquement (ReportLab), téléchargeable depuis le dashboard
  (propriétaire uniquement — plus d'accès public)
- Assistant IA (Groq) : génération/amélioration de bio, suggestions de
  compétences, analyse de profil, assistant conversationnel
- Admin Django configuré pour tous les modèles restants
- Toujours pas de paiement — plateforme gratuite

**Retiré** : portfolio (CRUD projets, page publique, 10 thèmes visuels),
QR code, dashboard analytics (vues/clics/visiteurs), SEO (meta/Open Graph —
n'avait de sens que pour une page publique indexée).

## 6. Identité visuelle

Toujours d'actualité, aucun changement lié au pivot CV (le design system
rouge/crème/noir + Anton/Inter/JetBrains Mono reste identique). Voir
sections précédentes de ce document pour le détail : palette, typographie
disciplinée (Anton limité au hero/logo/score), élément signature (bande
verticale), cartes à bordure fine, focus rouge sur tous les formulaires.

**Templates existants après nettoyage** :
```
templates/
├── base.html                        → navbar simplifiée (plus de "Projets"/"Statistiques"/"Voir mon profil")
├── home.html                        → landing 100% CV
├── accounts/login.html, register.html
└── profiles/
    ├── dashboard.html                → plus de tuile Projets/Thème/SEO, CV generate+download fusionnés
    ├── edit_profile.html
    ├── onboarding.html
    ├── social_links.html
    ├── skills.html
    ├── experiences.html
    └── educations.html
```

**Supprimés** : `templates/projects/*` (4 fichiers), `templates/profiles/public/*`
(10 thèmes portfolio), `templates/analytics/*`, `templates/profiles/edit_theme.html`,
`templates/profiles/edit_seo.html`, `static/img/theme-previews/*`,
`generate_theme_previews.py`.

## 7. Vérification effectuée cette session

Contrairement aux sessions précédentes (lecture de code uniquement), cette
fois le retrait a été **vérifié par exécution réelle** :
- `python manage.py check` → aucune erreur
- `python manage.py makemigrations` + `migrate` sur base propre → OK
  (migration `profiles/0004_...` retire proprement les champs obsolètes)
- Tests fonctionnels via `django.test.Client` (vraies requêtes HTTP,
  pas de la lecture de code) :
  - Page d'accueil, dashboard, tous les formulaires (profil, compétences,
    expériences, formations, réseaux sociaux) → 200
  - Génération de CV (POST) → redirect 302, PDF bien généré
  - Téléchargement du CV → 200, `Content-Type: application/pdf`
  - Login/register (anonyme) → 200
  - `/u/<username>/`, `/projects/`, `/analytics/` → 404 confirmé (bien supprimés)

**Non vérifié** : rendu visuel réel en navigateur (toujours pas de
navigateur dans cet environnement).

## 8. Ce qui n'est PAS implémenté (hors périmètre actuel)

- Paiement / abonnements (décision explicite : plateforme gratuite)
- Le nouveau catalogue de thèmes CV + pipeline IA vision (voir section 9 —
  c'est le prochain chantier, pas encore commencé)
- Domaine personnalisé, comptes Business multi-profils, API publique
- Déploiement production (PostgreSQL, stockage objet, serveur applicatif)
- Tests automatisés (pytest/Django TestCase — les vérifications de cette
  session étaient des smoke tests manuels ponctuels, pas une suite de
  tests conservée dans le repo)

## 9. Prochain chantier — catalogue de thèmes CV + génération IA (à construire)

C'est la prochaine grosse étape, pas encore commencée. Élements validés
avec l'utilisateur :
- Nouveau modèle Django (ex. `CVTheme`) avec : nom, image de référence
  (uploadée par l'utilisateur lui-même via l'admin Django, pas par Claude),
  description optionnelle, et une "fiche de style" (JSON) remplie par
  analyse IA vision de l'image (palette, typographie, archétype de mise en
  page).
- Page de sélection de thème pour l'utilisateur final (catalogue avec
  images, façon de l'ancien `edit_theme.html` mais pour CV).
- Pipeline de génération : au moment de générer le CV, si la fiche de style
  du thème choisi n'est pas encore calculée, l'IA vision (modèle Groq à
  déterminer — à vérifier s'il propose un modèle vision) l'analyse une
  fois et la met en cache sur le `CVTheme`. Le CV est ensuite rendu par un
  moteur **paramétrable** (probablement plusieurs archétypes de mise en
  page ReportLab codés à l'avance, chacun paramétré par couleur/police
  selon la fiche de style) plutôt que du code généré à la volée par l'IA —
  pour garantir un rendu toujours propre et professionnel.
- Point technique à trancher à la reprise : rester sur ReportLab (portable,
  fonctionne partout y compris Windows) avec un nombre limité d'archétypes
  de mise en page codés à l'avance, vs. passer à un moteur HTML/CSS→PDF
  (ex. WeasyPrint, plus flexible pour du style piloté par variables CSS,
  mais dépendances système risquées sur Windows — l'environnement de dev
  de l'utilisateur, voir section 10).

## 10. Installation / lancement (rappel)

```bash
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env          # puis ajouter GROQ_API_KEY si besoin
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

⚠️ Comme le modèle `Profile` a changé (champs retirés), si tu avais une
base `db.sqlite3` existante avec l'ancien schéma, il faudra soit repartir
d'une base fraîche (`rm db.sqlite3` puis `migrate`), soit vérifier que la
migration `profiles/0004_...` s'applique proprement dessus.

## 11. Prochaines étapes suggérées (dans l'ordre)

1. **Vérifier visuellement en navigateur réel** (`python manage.py runserver`) —
   toujours pas fait, l'environnement de dev n'a pas de navigateur.
2. **Chantier catalogue de thèmes CV** (section 9) : concevoir le modèle
   `CVTheme`, l'interface admin pour que l'utilisateur uploade ses images,
   la page de sélection côté utilisateur final, et prototyper le pipeline
   IA vision (analyse d'image → fiche de style → CV généré).
3. Trancher ReportLab-paramétrique vs WeasyPrint pour le rendu final
   (impact sur la compatibilité Windows de l'utilisateur).
