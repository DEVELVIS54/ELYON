from django.urls import path

from . import views

app_name = 'ai'

urlpatterns = [
    path('bio/generate/', views.generate_bio, name='bio_generate'),
    path('bio/improve/', views.improve_bio, name='bio_improve'),
    path('skills/suggest/', views.suggest_skills, name='skill_suggestions'),
    path('profile/analyze/', views.analyze_profile, name='profile_analysis'),
    path('assistant/', views.assistant, name='assistant'),
]
