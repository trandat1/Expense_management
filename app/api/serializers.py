from rest_framework import serializers
from .models import Customers, Expense, History


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ("id", "name", "email", "password", "image")


class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ("id", "name", "email", "password", "image")


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("customer", "amount", "rent", "food", "saving", "orther", "date")


class CreateExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("customer", "amount", "rent", "food", "saving", "orther", "date")


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ("customer", "date", "amount", "description", "fields")


class CreateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ("customer", "date", "amount", "description", "fields")
