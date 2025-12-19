from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Job, Resume
import json

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary']

class ResumeForm(forms.ModelForm):
    skills = forms.CharField(widget=forms.Textarea, help_text="Enter skills separated by commas")
    work_experience = forms.CharField(widget=forms.Textarea, required=False)
    education = forms.CharField(widget=forms.Textarea, required=False)
    projects = forms.CharField(widget=forms.Textarea, required=False)
    certifications = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Resume
        fields = ['name', 'template_type', 'full_name', 'email', 'phone', 'address', 'linkedin', 'github', 'summary', 'skills', 'work_experience', 'education', 'projects', 'certifications']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['skills'].initial = ', '.join(self.instance.skills)
            self.fields['work_experience'].initial = self.instance.work_experience
            self.fields['education'].initial = self.instance.education
            self.fields['projects'].initial = self.instance.projects
            self.fields['certifications'].initial = self.instance.certifications

    def clean_skills(self):
        skills = self.cleaned_data['skills']
        return [skill.strip() for skill in skills.split(',') if skill.strip()]


