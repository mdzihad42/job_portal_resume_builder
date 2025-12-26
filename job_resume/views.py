from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None
from django.db.models import Q
import json
from .models import User, Job, Application, Resume, UserProfile
from .forms import UserRegistrationForm, JobForm, ResumeForm, JobApplicationForm, UserProfileForm
from .decorators import employer_required, admin_required, job_seeker_required

# Authentication Views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('job_resume:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('job_resume:admin_dashboard')
            elif user.role == 'employer':
                return redirect('job_resume:my_jobs')
            else:  # job_seeker
                return redirect('job_resume:home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('job_resume:home')

# Job Portal Views
@login_required
def home(request):
    if request.user.role == 'admin':
        jobs = Job.objects.all().order_by('-created_at')[:10]
    elif request.user.role == 'employer':
        jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')[:10]
    else:  # job_seeker
        jobs = Job.objects.filter(status='approved').order_by('-created_at')[:10]
    return render(request, 'home.html', {'jobs': jobs})

@login_required
def job_list(request):
    query = request.GET.get('q', '')
    if request.user.role == 'admin':
        jobs = Job.objects.all().order_by('-created_at')
    elif request.user.role == 'employer':
        jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    else:  # job_seeker
        jobs = Job.objects.filter(status='approved').order_by('-created_at')
        if query:
            jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(company__icontains=query) |
                Q(location__icontains=query)
            )
    return render(request, 'job_list.html', {'jobs': jobs, 'query': query})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = Application.objects.filter(user=request.user, job=job).exists()
    return render(request, 'job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
@job_seeker_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job_resume:my_applications')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm()
    return render(request, 'apply_job.html', {'job': job, 'form': form})

@login_required
@job_seeker_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-applied_at')
    return render(request, 'my_applications.html', {'applications': applications})

# Employer Views
@login_required
@employer_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_resume:my_jobs')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

@login_required
@employer_required
def my_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'my_jobs.html', {'jobs': jobs})

@login_required
@employer_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job).order_by('-applied_at')
    return render(request, 'job_applications.html', {'job': job, 'applications': applications})

@login_required
@employer_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['shortlisted', 'rejected', 'hired']:
            application.status = status
            application.save()
            messages.success(request, f'Application status updated to {status}!')
        return redirect('job_resume:job_applications', job_id=application.job.id)
    return render(request, 'update_application_status.html', {'application': application})

# Resume Builder Views
@login_required
@job_seeker_required
def resume_builder(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'Resume saved successfully!')
            return redirect('job_resume:my_resumes')
    else:
        form = ResumeForm()
    return render(request, 'resume_builder.html', {'form': form})

@login_required
@job_seeker_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume updated successfully!')
            return redirect('job_resume:my_resumes')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resume_builder.html', {'form': form, 'resume': resume})

@login_required
@job_seeker_required
def resume_preview(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return render(request, f'resume_{resume.template_type}.html', {'resume': resume})

@login_required
@job_seeker_required
def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    template = get_template(f'resume_{resume.template_type}.html')
    html = template.render({'resume': resume})
    if pisa is None:
        return HttpResponse('PDF generation is currently unavailable. Please contact support.', status=503)
        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.name}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
@job_seeker_required
def my_resumes(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'my_resumes.html', {'resumes': resumes})

# User Profile View
@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    edit_mode = request.GET.get('edit', False)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('job_resume:user_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user_profile.html', {
        'form': form,
        'profile': profile,
        'edit_mode': edit_mode
    })

# Admin Views
@login_required
@admin_required
def admin_dashboard(request):
    users = User.objects.all().order_by('-date_joined')
    jobs = Job.objects.all().order_by('-created_at')
    applications = Application.objects.all().order_by('-applied_at')
    
    # Simple analytics
    total_users = users.count()
    total_jobs = jobs.count()
    total_applications = applications.count()
    recent_users = users[:5]
    recent_jobs = jobs[:5]
    
    return render(request, 'admin_dashboard.html', {
        'users': users,
        'jobs': jobs,
        'applications': applications,
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'recent_users': recent_users,
        'recent_jobs': recent_jobs
    })

@login_required
@admin_required
def approve_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.status = 'approved'
    job.save()
    messages.success(request, 'Job approved successfully!')
    return redirect('job_resume:admin_dashboard')

@login_required
@admin_required
def reject_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.status = 'rejected'
    job.save()
    messages.success(request, 'Job rejected successfully!')
    return redirect('job_resume:admin_dashboard')

@login_required
@admin_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    messages.success(request, 'Job deleted successfully!')
    return redirect('job_resume:admin_dashboard')

@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'Cannot delete superuser!')
    else:
        user.delete()
        messages.success(request, 'User deleted successfully!')
    return redirect('job_resume:admin_dashboard')

@login_required
@admin_required
def manage_users(request):
    # This might be redundant if we put everything in dashboard, but keeping it for safety
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'manage_users.html', {'users': users})

@login_required
@admin_required
def change_user_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['job_seeker', 'employer', 'admin']:
            user.role = new_role
            user.save()
            messages.success(request, f'User role changed to {new_role}!')
        return redirect('job_resume:admin_dashboard')
    # If we want a separate page, we render 'change_user_role.html'.
    # implementing a simple redirect back if GET for now to avoid creating another template unless needed.
    return redirect('job_resume:admin_dashboard')

@login_required
@admin_required
def analytics_dashboard(request):
    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()
    approved_jobs = Job.objects.filter(status='approved').count()
    pending_jobs = Job.objects.filter(status='pending').count()
    return render(request, 'analytics_dashboard.html', {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'approved_jobs': approved_jobs,
        'pending_jobs': pending_jobs,
    })
