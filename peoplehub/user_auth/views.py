from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

# Create your views here.
class LoginAPIView(APIView):
    authentication_classes = []  # Disable authentication for login
    permission_classes = []  # Disable permission checks for login
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistration(APIView):
    authentication_classes = []  # Disable authentication for registration
    permission_classes = []  # Disable permission checks for registration

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User Created Successfully'}, status=status.HTTP_201_CREATED)
    
class LogoutAPIView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
