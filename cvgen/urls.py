from django.urls import path

from . import views

app_name = 'cvgen'

urlpatterns = [
    path('generate/', views.generate_cv, name='generate'),
    path('download/', views.download_cv, name='download'),
]
