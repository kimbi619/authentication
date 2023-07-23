

from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.GCEView.as_view()),
    path('image/', views.GceCertificateView.as_view()),
    path('subjects/', views.SubjectAPIView.as_view()),
    path('validate/', views.ValidateResultView.as_view()),
    path('validate/<int:id>/', views.ValidateRequirementAPIView.as_view()),
    path('requirements/', views.RestrictApiView.as_view()),
    path('requirements/<int:id>/', views.InstitutionRequirementAPIView.as_view()),
    path('admission-requirements/<int:id>/', views.AdmissionRequirementView.as_view(), name='admission-requirements-update'),
]