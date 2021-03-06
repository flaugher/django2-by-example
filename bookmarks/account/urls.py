from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    # account/login/
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # account/logout/
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # account/dashboard/
    path('', views.dashboard, name='dashboard'),
    # account/password_change/
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # account/password_change/done/
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # account/password_reset/
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # account/password_reset/done/
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # account/reset/Mjg/a12345/
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # account/reset/done/
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # account/register/
    path('register/', views.register, name='register'),
    # account/edit/
    path('edit/', views.edit, name='edit'),
    # account/users/
    path('users/', views.user_list, name='user_list'),
    # account/users/follow/
    # This must precede the user_detail pattern.
    path('users/follow/', views.user_follow, name="user_follow"),
    # account/users/johndoe/
    path('users/<username>/', views.user_detail, name='user_detail'),
]
