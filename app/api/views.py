from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    ExpenseSerializer,
    CreateExpenseSerializer,
    HistorySerializer,
    CreateHistorySerializer,
)
from .models import Expense, History
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UsersView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]  # Thêm dòng này

    def get(self, request, *args, **kwargs):
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)
    
class CreateUserView(APIView):
    serializer_class = CreateUserSerializer
#   permission_classes = [IsAuthenticated]  # Thêm dòng này
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)