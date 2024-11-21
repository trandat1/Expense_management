from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Expense, History, Profile
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, default="static/images/uploads/account-icon-user-icon-vector-graphics_292645-552.avif")

    class Meta:
        model = Profile
        fields = ("image", "sex", "birth")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    token = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = ("id", "token","username", "email", "profile")

    def get_token(self, obj):
        if self.context.get("include_token", False):
            token = Token.objects.get(user=obj)
            return token.key
        return ""

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
    token = serializers.SerializerMethodField(required=False)
    class Meta:
        model = User
        fields = ("id","token", "username", "email", "password", "profile")
    
    def get_token(self, obj):
        if self.context.get("include_token", False):
            token = Token.objects.get(user=obj)
            return token.key
        return ""


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("user", "amount", "rent", "food", "saving", "orther", "date")


class CreateExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("user", "amount", "rent", "food", "saving", "orther", "date")


class HistorySerializer(serializers.ModelSerializer):
    # balance = serializers.SerializerMethodField()
    class Meta:
        model = History
        fields = ("user", "date", "amount", "description", "field","balance")
    

class CreateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['date', 'amount', 'description', 'field', 'balance']  # Liệt kê các trường cần trả về

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'date' in data and instance.date:
            # Chuyển đổi datetime thành date dạng `YYYY-MM-DD`
            data['date'] = instance.date.isoformat()  # Chỉ giữ phần ngày
        return data
