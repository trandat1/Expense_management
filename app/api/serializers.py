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
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "token", "username", "email", "profile")

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class CreateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "token", "username", "email", "password", "profile")

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id","token", "username", "email", "password", "profile")
    
    def get_token(self, obj):
        token = Token.objects.get(user=obj)
        return token.key


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
