from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.generics import GenericAPIView

# Create your views here.
from .models import User
from .serializers import RegisterSerializer


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    # def get(self, request):
    #     user = User.objects.all()
    #     serializer = self.serializer_class(user, many=True)
    #     return Response( serializer.data, status=status.HTTP_200_OK )
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_201_CREATED )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )
    