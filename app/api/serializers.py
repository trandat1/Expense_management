from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Expense, History, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    

    class Meta:
        model = Profile
        fields = ("image", "sex", "birth")

class CreateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "profile")

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        print(profile_data)
        image = profile_data.get("image",None)
        sex = profile_data.get("sex", None)
        birth = profile_data.get("birth", None)
        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        if image is not None:
            user.profile.image = image
        if sex is not None:
            user.profile.sex = sex
        if birth is not None:
            user.profile.birth = birth
        user.profile.save()

        return user


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
