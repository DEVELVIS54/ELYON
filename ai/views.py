import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from . import services
from .models import AIRequest


def _profile_summary(profile):
    return {
        "profession": profile.profession,
        "bio": profile.bio,
        "skills": [s.name for s in profile.skills.all()],
        "has_github": profile.social_links.filter(platform='github').exists(),
        "has_linkedin": profile.social_links.filter(platform='linkedin').exists(),
        "score": profile.professional_score,
    }


def _save_request(user, request_type, prompt_input, output):
    AIRequest.objects.create(
        user=user, request_type=request_type,
        prompt_input=prompt_input, response_output=output,
    )


def _handle(request, request_type, fn, prompt_input):
    try:
        result = fn()
    except services.AIServiceError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
    _save_request(request.user, request_type, prompt_input, str(result))
    return JsonResponse({"ok": True, "result": result})


@login_required
@require_POST
def generate_bio(request):
    profile = request.user.profile
    body = json.loads(request.body or '{}')
    skills = body.get('skills') or ', '.join(s.name for s in profile.skills.all())
    experience = body.get('experience_years', 'non précisé')
    return _handle(
        request, 'bio_generate',
        lambda: services.generate_bio(profile.profession, skills, experience),
        prompt_input=f"profession={profile.profession}, skills={skills}",
    )


@login_required
@require_POST
def improve_bio(request):
    body = json.loads(request.body or '{}')
    raw_text = body.get('text', '')
    if not raw_text.strip():
        return JsonResponse({"ok": False, "error": "Aucun texte fourni."}, status=400)
    return _handle(
        request, 'bio_improve',
        lambda: services.improve_bio(raw_text),
        prompt_input=raw_text,
    )


@login_required
@require_POST
def suggest_skills(request):
    profile = request.user.profile
    existing = ', '.join(s.name for s in profile.skills.all())
    return _handle(
        request, 'skill_suggestions',
        lambda: services.suggest_skills(profile.profession, existing),
        prompt_input=existing,
    )


@login_required
@require_POST
def analyze_profile(request):
    profile = request.user.profile
    summary = _profile_summary(profile)
    return _handle(
        request, 'profile_analysis',
        lambda: services.analyze_profile(json.dumps(summary, ensure_ascii=False)),
        prompt_input=json.dumps(summary, ensure_ascii=False),
    )


@login_required
@require_POST
def assistant(request):
    profile = request.user.profile
    body = json.loads(request.body or '{}')
    question = body.get('question', '')
    if not question.strip():
        return JsonResponse({"ok": False, "error": "Pose une question."}, status=400)
    summary = json.dumps(_profile_summary(profile), ensure_ascii=False)
    return _handle(
        request, 'assistant',
        lambda: services.ask_assistant(question, summary),
        prompt_input=question,
    )
