from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    CustomerSerializer,
    CreateCustomerSerializer,
    ExpenseSerializer,
    CreateExpenseSerializer,
    HistorySerializer,
    CreateHistorySerializer,
)
from .models import Customers, Expense, History
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UsersView(APIView):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticated]  # Thêm dòng này

    def get(self, request, *args, **kwargs):
        customers = self.queryset.all()
        serializer = self.serializer_class(customers, many=True)
        return Response(serializer.data)
    
class CreateUserView(APIView):
    serializer_class = CreateCustomerSerializer
#   permission_classes = [IsAuthenticated]  # Thêm dòng này
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)