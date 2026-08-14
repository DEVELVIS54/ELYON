from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import redirect

from .services import build_cv_pdf


@login_required
def generate_cv(request):
    """Génère le CV du profil connecté et le stocke sur le modèle Profile."""
    profile = request.user.profile
    buffer = build_cv_pdf(profile)
    filename = f"cv_{profile.user.username}.pdf"
    profile.cv_pdf.save(filename, ContentFile(buffer.getvalue()), save=True)
    messages.success(request, "Ton CV a été généré avec succès.")
    return redirect('profiles:dashboard')


@login_required
def download_cv(request):
    """Téléchargement du CV du profil connecté — génère à la volée si absent."""
    profile = request.user.profile

    if profile.cv_pdf:
        pdf_bytes = profile.cv_pdf.read()
    else:
        buffer = build_cv_pdf(profile)
        pdf_bytes = buffer.getvalue()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cv_{profile.user.username}.pdf"'
    return response
