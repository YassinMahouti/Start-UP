from django.http import HttpResponse
from django.shortcuts import redirect


# Stop authenticated users from seeing the login and registration screen
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user-page')
        else:
            return view_func(*args, **kwargs)
    return wrapper_func
