

from django.urls import path
from .views import GCEView

urlpatterns = [
    path('register/', GCEView.as_view()),
]