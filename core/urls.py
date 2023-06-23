
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='Register'),
    path('login/', LoginAPIView.as_view(), name='Login'),
    path('user/', UserView.as_view(), name='User'),
]