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
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detailed job description...', 'rows': 5}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Location'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary (e.g. 50000)'}),
        }

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
    # Explicitly defined fields with widgets
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Python, JavaScript, Django...'}),
        help_text="Enter skills separated by commas"
    )
    work_experience = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Software Engineer at Google (2020-Present)...'}),
        required=False
    )
    education = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'BS Computer Science, MIT (2016-2020)...'}),
        required=False
    )
    projects = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'E-commerce Platform: Built with Django...'}),
        required=False
    )
    certifications = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'AWS Certified Solutions Architect...'}),
        required=False
    )

    class Meta:
        model = Resume
        fields = ['name', 'template_type', 'full_name', 'email', 'phone', 'address', 'linkedin', 'github', 'summary', 'skills', 'work_experience', 'education', 'projects', 'certifications']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. My Tech Resume'}),
            'template_type': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 890'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/john'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/john'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief professional summary...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Handle list to string conversion for skills if it's stored as a list
            if isinstance(self.instance.skills, list):
                self.fields['skills'].initial = ', '.join(self.instance.skills)
            else:
                self.fields['skills'].initial = self.instance.skills
            
            # Populate other text fields from the model
            self.fields['work_experience'].initial = self.instance.work_experience
            self.fields['education'].initial = self.instance.education
            self.fields['projects'].initial = self.instance.projects
            self.fields['certifications'].initial = self.instance.certifications

    def clean_skills(self):
        skills = self.cleaned_data.get('skills', '')
        if not skills:
            return []
        # Return as a list of strings
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




