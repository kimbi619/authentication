

from django.urls import path
from .views import GCEView

urlpatterns = [
    path('results/', GCEView.as_view()),
]