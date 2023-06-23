

from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.GCEView.as_view()),
    path('image/', views.GceCertificateView.as_view()),
]