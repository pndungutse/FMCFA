from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# from django.template.loader import render_to_string


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('render_404')
        return wrapper_func
    return decorator
           

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.filter(name='hospital')==True:
            return redirect('hos_dashboard')
        elif request.user.groups.filter(name='pharmacy')==True:
            return redirect('phar_dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func