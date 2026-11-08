from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializer import TodoSerializer
from .models import Todo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.
class TodoListCreateView(ListCreateAPIView):
    # queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class TodoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    
class ROOTAPIView(APIView):
    def get(self, request):
        return Response({
            'list': reverse('list', request=request),
        })