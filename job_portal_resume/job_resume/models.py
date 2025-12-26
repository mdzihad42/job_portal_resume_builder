from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator

# Custom User model with roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')

    def __str__(self):
        return self.username

# User Profile model for additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Personal Information
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Professional Information
    bio = models.TextField(blank=True, help_text="Brief professional summary")
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    # Company Information (for employers)
    company_name = models.CharField(max_length=100, blank=True)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)

    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Preferences
    email_notifications = models.BooleanField(default=True)
    profile_visibility = models.BooleanField(default=True, help_text="Make profile visible to other users")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def display_name(self):
        return self.full_name or self.user.get_full_name() or self.user.username

# Job model
class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Application model
class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, default='')
    cv_pdf = models.FileField(upload_to='applications/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

# Resume model
class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('classic', 'Classic Professional'),
        ('modern', 'Modern Tech'),
        ('creative', 'Creative Professional'),
        ('executive', 'Executive CV'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    template_type = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')
    name = models.CharField(max_length=100, default='My Resume')

    # Personal Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    # Professional Summary
    summary = models.TextField(blank=True)

    # Skills
    skills = models.JSONField(default=list)  # List of skills

    # Work Experience
    work_experience = models.TextField(blank=True)

    # Education
    education = models.TextField(blank=True)

    # Projects
    projects = models.TextField(blank=True)

    # Certifications
    certifications = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"
