from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from actions.models import Action
from actions.utils import create_action
from common.decorators import ajax_required

from .forms import (LoginForm, ProfileEditForm, UserEditForm,
                    UserRegistrationForm)
from .models import Contact, Profile


@login_required
def dashboard(request):
    """Display dashboard when users log into their account."""
    # Get all actions excluding those performed by the current user.
    actions = Action.objects.exclude(user=request.user)

    # Check if the current user is following other users.
    # We added the 'following' field to the User class in the account model.
    following_ids = request.user.following.values_list('id', flat=True)

    # If user is following other users, retrieve only their actions
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    # Limit results to last 10 actions returned. This assumes the default ordering as defined in the Action class's Meta class specifies order by last created.
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]
    # With 'select_related', the above query not only gets all the actions performed by the current user but it also accesses the profile of the user associated with each action.  Recall that the Profile model is an extension of the User model.

    return render(request,
        'account/dashboard.html',
        { 'section': 'dashboard', 'actions': actions })

@login_required
def edit(request):
    """User can edit their profile."""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
        {'user_form': user_form, 'profile_form': profile_form})

def register(request):
    """Register a new user."""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but don't save it to the database yet.
            new_user = user_form.save(commit=False)
            # Set the chosen password using set_password which will handle the encryption for us.
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the user object to the database.
            new_user.save()
            # Create the user's profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def user_detail(request, username):
    """Show details for a user."""
    user = get_object_or_404(User,
        username=username,
        is_active=True)
    return render(request,
        'account/user/detail.html',
        {'section': 'people',
        'user': user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    """Follow or unfollow a user."""
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from = request.user, user_to = user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                    user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


@login_required
def user_list(request):
    """Get all active users."""
    users = User.objects.filter(is_active=True)
    return render(request,
        'account/user/list.html',
        {'section': 'people',
        'users': users})

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
