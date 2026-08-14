from django.contrib import admin

from .models import AIRequest


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_type', 'created_at')
    list_filter = ('request_type',)
    readonly_fields = ('prompt_input', 'response_output', 'created_at')
