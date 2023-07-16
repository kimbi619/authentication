from rest_framework import serializers
from .models import Result, Student, Certificate, Institution, AdmissionRequirement
from core.models import User

class StudentSerializer(serializers.ModelSerializer):
    model = Student
    fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    model = Result
    fields = ['subject', 'grade', 'level']

class GceCertificateSerializer(serializers.ModelSerializer):
    model = Certificate
    fields = ['certificate']


class RequirementTitleSerializer(serializers.ModelSerializer):
    model = Institution
    fields = '__all__'


class InstitutionSerializer(serializers.ModelSerializer):
    requirements = Institution
    fields = '__all__'
    

class AdmissionRequirementSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = AdmissionRequirement
        fields = ['id', 'institution', 'subject', 'grade']

        read_only_fields = ['institution']

 
class InstitutionSerializer(serializers.ModelSerializer):
    admission_requirements = AdmissionRequirementSerializer(many=True)

    class Meta:
        model = Institution
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        requirements_data = validated_data.pop('admission_requirements')
        
        user_id = validated_data.get('user_id')
        user = User.objects.filter(id=user_id).first()
        validated_data['user_id'] = user

        institution = Institution.objects.create(**validated_data)

        for requirement_data in requirements_data:
            AdmissionRequirement.objects.create(**requirement_data, institution=institution)
        return institution