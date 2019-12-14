from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # account/dashboard/
    path('', views.dashboard, name='dashboard'),
    # account/password_change/
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # account/password_change/done/
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
