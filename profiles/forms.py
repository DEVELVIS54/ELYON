from django import forms

from .models import Education, Experience, Profile, SocialLink, Skill


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'photo', 'full_name', 'profession', 'location', 'bio',
            'email_public', 'phone', 'availability',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'school', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
