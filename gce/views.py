from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView, Response, status
from .serializers import ResultSerializer, StudentSerializer
from .models import Result, Student
from .data.filterList import fetchAllData

class GCEView(APIView):
    def get(self, request):
        name = request.data.get('name', None)
        level = request.data.get('level', None)
        student = Student.objects.filter(name = name).first()
        # studentSerializer = StudentSerializer(student)
        print(student)
        return Response({"message": "accepted"}, status=status.HTTP_200_OK)


# class Create(APIView):
#     def post(self, request):
#         body = self.request.body

#         print(body)

#         return Response({"message": "meet me"}, status=status.HTTP_200_OK)
    

# def populateDB():
#     data = fetchAllData()
#     for dataItem in data:
#         name = dataItem['name']
#         grades = dataItem['grades']
#         new_student = Student.objects.create(name=name)

# populateDB()