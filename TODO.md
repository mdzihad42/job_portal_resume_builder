# TODO List for Job Portal with Resume Builder

## 1. Update Django Settings
- [x] Add 'job_resume' to INSTALLED_APPS in settings.py
- [x] Configure STATIC_URL, STATICFILES_DIRS, MEDIA_URL, MEDIA_ROOT
- [x] Add authentication settings if needed

## 2. Define Models
- [x] Create custom User model or extend AbstractUser for roles (Job Seeker, Employer, Admin)
- [x] Job model: title, description, company, location, salary, etc.
- [x] Application model: user, job, status, applied_date
- [x] Resume model: user, template_type, personal_info, summary, skills, experience, education, projects, certifications
- [x] Run migrations

## 3. Create Views
- [x] Authentication views: register, login, logout
- [x] Job views: list jobs, job detail, apply for job
- [x] Employer views: post job, manage applications
- [x] Resume Builder views: create/edit resume, select template, preview, download PDF
- [x] Admin views: dashboard for managing users, jobs, reports

## 4. URL Configuration
- [x] Create job_resume/urls.py
- [x] Include job_resume URLs in main urls.py

## 5. Templates and Static Files
- [x] Create base.html template
- [x] Templates for login, register, job list, job detail, resume builder, etc.
- [x] Add CSS/JS for responsive, professional design
- [x] Implement resume template styles (Classic, Modern, Creative, Executive)

## 6. Additional Features
- [x] PDF generation for resumes (using xhtml2pdf)
- [x] Live preview for resume editing
- [x] Drag-and-drop for sections
- [x] Save multiple resumes per user
- [x] Secure authentication

## 7. Testing and Deployment
- [ ] Test all features
- [ ] Ensure responsive design
- [ ] Production settings (DEBUG=False, etc.)
