from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


def user_login(request):
    """Log a user in."""
    # Process login form on POST.
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,    # Check the user's credentials.
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)    # Set the user in the current session.
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        # Display login form on GET.
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    """Display dashboard when users log into their account."""
    return render(request,
        'account/dashboard.html',
        { 'section': 'dashboard' })