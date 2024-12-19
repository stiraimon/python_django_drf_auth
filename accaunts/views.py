from django.shortcuts import render
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .serializers import UserSerializer

from . import serializers


class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = serializers.LoginSerializers(data=self.request.data, context={ 'request': self.request})
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
    def get(self, request):
        users = User.objects.all()
        serializer =  UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    
class LogoutView(views.APIView):
    def logout(self, request):
        logout(request)
        return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)

