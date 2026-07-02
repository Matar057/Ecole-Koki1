from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

User = get_user_model()


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            if request.user.role not in roles:
                messages.error(request, 'Vous n\'avez pas la permission d\'accéder à cette page.')
                return redirect('dashboard:home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
