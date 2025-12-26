from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Job, Resume, Application, UserProfile
import json

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[c for c in User.ROLE_CHOICES if c[0] != 'admin'], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary']

class JobApplicationForm(forms.ModelForm):
    cv_pdf = forms.FileField(
        required=True,
        label="Upload CV (PDF only)",
        help_text="Please upload your CV in PDF format",
        widget=forms.FileInput(attrs={'accept': '.pdf'})
    )

    class Meta:
        model = Application
        fields = ['name', 'phone', 'cv_pdf']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone', 'address', 'date_of_birth', 'bio', 'linkedin_url', 'github_url', 'portfolio_url', 'company_name', 'company_website', 'company_description', 'profile_picture', 'email_notifications', 'profile_visibility']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
            'company_description': forms.Textarea(attrs={'rows': 3}),
        }




