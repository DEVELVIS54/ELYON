from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('onboarding/', views.onboarding, name='onboarding'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.edit_profile, name='edit_profile'),

    path('dashboard/social-links/', views.manage_social_links, name='social_links'),
    path('dashboard/social-links/<int:pk>/delete/', views.delete_social_link, name='delete_social_link'),

    path('dashboard/skills/', views.manage_skills, name='skills'),
    path('dashboard/skills/<int:pk>/delete/', views.delete_skill, name='delete_skill'),

    path('dashboard/experiences/', views.manage_experiences, name='experiences'),
    path('dashboard/experiences/<int:pk>/delete/', views.delete_experience, name='delete_experience'),

    path('dashboard/educations/', views.manage_educations, name='educations'),
    path('dashboard/educations/<int:pk>/delete/', views.delete_education, name='delete_education'),
]
