from django.db.migrations import serializer
from django.shortcuts import render
from .models import Person
from .serializers import PersonModelSerializer
from  rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser 
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

# Create your views here.
@api_view(['GET', 'PUT', 'PATCH']) 
def singleobj(request, id):
    # data = Person.objects.get(id=id) 
    data = get_object_or_404(Person, id=id)

    if request.method == "PUT":
        parsed_data = request.data
        serializer = PersonModelSerializer(data, data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'update': 'successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "PATCH":
        parsed_data = request.data
        serializer = PersonModelSerializer(data, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'update': 'successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        serializer = PersonModelSerializer(data)
        return Response(serializer.data)
   
@api_view(['GET', 'POST'])
def multipleobj(request):
    if request.method == 'POST':
        parsed_data = request.data
        serializer = PersonModelSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created": "successful "}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    if request.method == "GET":         
        data = Person.objects.all()
        serializer = PersonModelSerializer(data, many=True)
        return Response(serializer.data)
    
    
class MultipleObjAPIView(GenericAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Person.objects.all().order_by('id')
    serializer_class = PersonModelSerializer

    def get(self, request):
        print("User:", request.user)
        page = self.paginate_queryset(self.get_queryset())  # uses PAGE_SIZE from settings
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        parsed_data = request.data
        serializer = PersonModelSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created": "successful "}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SingleObjAPIView(APIView):
    def get(self, request, id):
        data = get_object_or_404(Person, id=id)
        serializer = PersonModelSerializer(data)
        return Response(serializer.data)
    
    def put(self, request, id):
        data = get_object_or_404(Person, id=id)
        parsed_data = request.data
        serializer = PersonModelSerializer(data, data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'update': 'successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        data = get_object_or_404(Person, id=id)
        parsed_data = request.data
        serializer = PersonModelSerializer(data, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'update': 'successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    