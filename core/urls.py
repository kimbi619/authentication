
from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='Register'),
    path('login/', views.LoginAPIView.as_view(), name='Login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.UserView.as_view(), name='get_user'),
    # path('confirm-user/', views.UserView.as_view(), name='User Confirm'),  
    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    path('password-reset/<uidb64>/<token>', views.RequestPasswordReset.as_view(), name='password_reset_confirm'),
    path('request-password-reset/', views.PasswordTokenCheck.as_view(), name='password_reset'),


] 