

from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.GCEView.as_view()),
    path('image/', views.GceCertificateView.as_view()),
    path('validate/', views.ValidateResultView.as_view()),
    path('requirements/', views.RestrictApiView.as_view()),
]