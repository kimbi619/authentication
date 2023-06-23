from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView, Response, status
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate

# Create your views here.
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_201_CREATED )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )
    

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password = password)
        
        if not user:
            return Response({"message": "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.serializer_class(user)

        # if serializer.is_valid():
        #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED )
        # return Response('valid user, unknown serializer')
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

        
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)