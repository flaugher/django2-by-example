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
    # account/password_reset/
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # account/password_reset/done/
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # account/reset/Mjg/a12345/
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # account/reset/done/
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
