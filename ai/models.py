from django.conf import settings
from django.db import models


class AIRequest(models.Model):
    REQUEST_TYPES = [
        ('bio_generate', 'Génération de bio'),
        ('bio_improve', 'Amélioration de bio'),
        ('skill_suggestions', 'Suggestions de compétences'),
        ('profile_analysis', 'Analyse du profil'),
        ('assistant', 'Assistant professionnel'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_requests')
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES)
    prompt_input = models.TextField(blank=True)
    response_output = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.user}"
