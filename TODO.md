# TODO List for Job Portal with Resume Builder

## 1. Update Django Settings
- [ ] Add 'job_resume' to INSTALLED_APPS in settings.py
- [ ] Configure STATIC_URL, STATICFILES_DIRS, MEDIA_URL, MEDIA_ROOT
- [ ] Add authentication settings if needed

## 2. Define Models
- [ ] Create custom User model or extend AbstractUser for roles (Job Seeker, Employer, Admin)
- [ ] Job model: title, description, company, location, salary, etc.
- [ ] Application model: user, job, status, applied_date
- [ ] Resume model: user, template_type, personal_info, summary, skills, experience, education, projects, certifications
- [ ] Run migrations

## 3. Create Views
- [ ] Authentication views: register, login, logout
- [ ] Job views: list jobs, job detail, apply for job
- [ ] Employer views: post job, manage applications
- [ ] Resume Builder views: create/edit resume, select template, preview, download PDF
- [ ] Admin views: dashboard for managing users, jobs, reports

## 4. URL Configuration
- [ ] Create job_resume/urls.py
- [ ] Include job_resume URLs in main urls.py

## 5. Templates and Static Files
- [ ] Create base.html template
- [ ] Templates for login, register, job list, job detail, resume builder, etc.
- [ ] Add CSS/JS for responsive, professional design
- [ ] Implement resume template styles (Classic, Modern, Creative, Executive)

## 6. Additional Features
- [ ] PDF generation for resumes (using reportlab or weasyprint)
- [ ] Live preview for resume editing
- [ ] Drag-and-drop for sections
- [ ] Save multiple resumes per user
- [ ] Secure authentication

## 7. Testing and Deployment
- [ ] Test all features
- [ ] Ensure responsive design
- [ ] Production settings (DEBUG=False, etc.)
