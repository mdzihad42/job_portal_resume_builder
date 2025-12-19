from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import json
from .models import User, Job, Application, Resume
from .forms import UserRegistrationForm, JobForm, ResumeForm
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
        jobs = Job.objects.all()[:10]
    elif request.user.role == 'employer':
        jobs = Job.objects.filter(posted_by=request.user)[:10]
    else:  # job_seeker
        jobs = Job.objects.all()[:10]
    return render(request, 'home.html', {'jobs': jobs})

@login_required
def job_list(request):
    if request.user.role == 'admin':
        jobs = Job.objects.all()
    elif request.user.role == 'employer':
        jobs = Job.objects.filter(posted_by=request.user)
    else:  # job_seeker
        jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

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
        Application.objects.create(user=request.user, job=job)
        messages.success(request, 'Application submitted successfully!')
        return redirect('job_resume:my_applications')
    return render(request, 'apply_job.html', {'job': job})

@login_required
@job_seeker_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user)
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
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'my_jobs.html', {'jobs': jobs})

@login_required
@employer_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job)
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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.name}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
@job_seeker_required
def my_resumes(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'my_resumes.html', {'resumes': resumes})

# Admin Views
@login_required
@admin_required
def admin_dashboard(request):
    users = User.objects.all()
    jobs = Job.objects.all()
    applications = Application.objects.all()
    return render(request, 'admin_dashboard.html', {
        'users': users,
        'jobs': jobs,
        'applications': applications
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
def manage_users(request):
    users = User.objects.all()
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
        return redirect('job_resume:manage_users')
    return render(request, 'change_user_role.html', {'user': user})

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
