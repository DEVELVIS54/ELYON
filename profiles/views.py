from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (EducationForm, ExperienceForm, ProfileForm,
                     SkillForm, SocialLinkForm)
from .models import Education, Experience, Profile, SocialLink, Skill


def home(request):
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')
    return render(request, 'home.html')


@login_required
def onboarding(request):
    """Formulaire simplifié affiché juste après l'inscription."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Ton profil est prêt. Bienvenue sur ELYON !")
            return redirect('profiles:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/onboarding.html', {'form': form})


@login_required
def dashboard(request):
    profile = request.user.profile
    context = {
        'profile': profile,
        'score': profile.professional_score,
        'missing_items': profile.missing_items,
    }
    return render(request, 'profiles/dashboard.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect('profiles:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})


# --- Social links ---------------------------------------------------

@login_required
def manage_social_links(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = profile
            link.save()
            messages.success(request, "Lien ajouté.")
            return redirect('profiles:social_links')
    else:
        form = SocialLinkForm()
    return render(request, 'profiles/social_links.html', {
        'form': form, 'links': profile.social_links.all(),
    })


@login_required
def delete_social_link(request, pk):
    link = get_object_or_404(SocialLink, pk=pk, profile=request.user.profile)
    link.delete()
    messages.success(request, "Lien supprimé.")
    return redirect('profiles:social_links')


# --- Skills -----------------------------------------------------------

@login_required
def manage_skills(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = profile
            skill.save()
            messages.success(request, "Compétence ajoutée.")
            return redirect('profiles:skills')
    else:
        form = SkillForm()
    return render(request, 'profiles/skills.html', {
        'form': form, 'skills': profile.skills.all(),
    })


@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, profile=request.user.profile)
    skill.delete()
    messages.success(request, "Compétence supprimée.")
    return redirect('profiles:skills')


# --- Experience ---------------------------------------------------------

@login_required
def manage_experiences(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = profile
            exp.save()
            messages.success(request, "Expérience ajoutée.")
            return redirect('profiles:experiences')
    else:
        form = ExperienceForm()
    return render(request, 'profiles/experiences.html', {
        'form': form, 'experiences': profile.experiences.all(),
    })


@login_required
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, profile=request.user.profile)
    exp.delete()
    messages.success(request, "Expérience supprimée.")
    return redirect('profiles:experiences')


# --- Education ------------------------------------------------------

@login_required
def manage_educations(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = profile
            edu.save()
            messages.success(request, "Formation ajoutée.")
            return redirect('profiles:educations')
    else:
        form = EducationForm()
    return render(request, 'profiles/educations.html', {
        'form': form, 'educations': profile.educations.all(),
    })


@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, profile=request.user.profile)
    edu.delete()
    messages.success(request, "Formation supprimée.")
    return redirect('profiles:educations')
