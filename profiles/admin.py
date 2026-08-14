from django.contrib import admin

from .models import Education, Experience, Profile, SocialLink, Skill


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'profession', 'plan', 'professional_score')
    list_filter = ('plan',)
    search_fields = ('user__username', 'full_name', 'profession')
    inlines = [SocialLinkInline, SkillInline]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'profile', 'start_date', 'end_date')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'profile', 'start_date')
