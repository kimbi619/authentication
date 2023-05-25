from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView, Response, status
from .serializers import ResultSerializer, StudentSerializer
from .models import Result, Student
from .data.filterList import fetchAllData
from django.core import serializers

class GCEView(APIView):
    def get(self, request):
        name = request.data.get('name', None)
        level = request.data.get('level', None)
        student = Student.objects.filter(name = name).first()

        grade = Result.objects.filter(student_id = student).all()
        print("the student grades....", grade)
        # serializer = ResultSerializer(grade, many=True)
        serialized_data = serializers.serialize('json', grade)
        print(serialized_data)
        return Response( serialized_data, status=status.HTTP_200_OK)


# class Create(APIView):
#     def post(self, request):
#         body = self.request.body

#         print(body)

#         return Response({"message": "meet me"}, status=status.HTTP_200_OK)
    

def populateDB():
    data = fetchAllData()
    for dataItem in data:
        name = dataItem['name']
        grades = dataItem['grades']
        new_student = Student.objects.create(name=name)
        for grade in grades:
            Result.objects.create(student_id=new_student, subject=grade['title'].strip(), grade=grade['grade'].strip(), level='ordinary', education='general')

# populateDB()