from django.urls import path
from . import views

app_name = 'job_resume'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Job Portal
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),

    # Employer
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('job/<int:job_id>/applications/', views.job_applications, name='job_applications'),

    # Resume Builder
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    path('resume/<int:resume_id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:resume_id>/preview/', views.resume_preview, name='resume_preview'),
    path('resume/<int:resume_id>/download/', views.download_resume, name='download_resume'),
    path('my-resumes/', views.my_resumes, name='my_resumes'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
