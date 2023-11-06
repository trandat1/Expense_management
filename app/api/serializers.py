from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Expense, History, Profile
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Profile
        fields = ("image", "sex", "birth")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "profile")


class CreateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "profile")


class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "profile")


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("user", "amount", "rent", "food", "saving", "orther", "date")


class CreateExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("user", "amount", "rent", "food", "saving", "orther", "date")


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ("user", "date", "amount", "description", "fields")


class CreateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ("user", "date", "amount", "description", "fields")
