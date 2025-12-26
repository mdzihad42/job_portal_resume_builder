from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Access denied. Insufficient permissions.')
                return redirect('job_resume:home')
        return _wrapped_view
    return decorator

# Specific decorators for convenience
def employer_required(view_func):
    return role_required(['employer'])(view_func)

def job_seeker_required(view_func):
    return role_required(['job_seeker'])(view_func)

def admin_required(view_func):
    return role_required(['admin'])(view_func)
