from rest_framework import serializers
from .models import Result, Student

class StudentSerializer(serializers.ModelSerializer):
    model = Student
    fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    model = Result
    fields = '__all__'