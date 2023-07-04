from rest_framework import serializers
from .models import Result, Student, Certificate

class StudentSerializer(serializers.ModelSerializer):
    model = Student
    fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    model = Result
    fields = ['subject', 'grade', 'level']

class GceCertificateSerializer(serializers.ModelSerializer):
    model = Certificate
    fields = ['certificate']