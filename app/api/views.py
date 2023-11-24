from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    ExpenseSerializer,
    CreateExpenseSerializer,
    HistorySerializer,
    CreateHistorySerializer,
)
from .models import Expense, History
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError

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
            try:
                # Tạo người dùng
                user = User(
                    email=request.data["email"], username=request.data["username"]
                )
                user.set_password(request.data["password"])
                user.save()
            except IntegrityError as e:
                if "unique constraint" in str(e):
                    return Response(
                        {"error": "A user with that email already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    print(e)
                    return Response(
                        {"error": "An error occurred while creating the user."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            profile_data = {}
            for key in ["profile.sex", "profile.birth", "profile.image"]:
                profile_data[key.split(".")[1]] = request.data.pop(key, None)
            image = profile_data.get("image", None)
            sex = profile_data.get("sex", None)
            birth = profile_data.get("birth", None)

            if image is not None:
                user.profile.image = image[0] if isinstance(image, list) else image
            if sex is not None:
                user.profile.sex = sex[0] if isinstance(sex, list) else sex
            if birth is not None:
                if isinstance(birth, str):
                    birth = datetime.fromisoformat(birth).date()
                elif isinstance(birth, list):
                    # Handle non-string birth value
                    birth = datetime.fromisoformat(birth[0]).date()
                else:
                    birth = None
                user.profile.birth = birth
            user.profile.save()
            profile_data_ = user.profile
            # print(user.profile)
            if image is not None:
                image = str(profile_data_.image)
                profile_data_.image = image.replace("frontend", "")
                profile_data_.save()
            return Response(
                self.serializer_class(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    serializer_class = UpdateUserSerializer

    def get(self, request, id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_id = id
        user_data = User.objects.get(id=user_id)
        if user_data:
            return Response(
                self.serializer_class(user_data).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    # permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        user_id = id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        data = request.data
        profile_data = {}
        for key in ["profile.sex", "profile.birth", "profile.image"]:
            profile_data[key.split(".")[1]] = request.data.pop(key, None)
        if profile_data:
            image = profile_data.get("image", None)
            sex = profile_data.get("sex", None)
            birth = profile_data.get("birth", None)

            user.profile.image = image[0] if isinstance(image, list) else image
            user.profile.sex = sex[0] if isinstance(sex, list) else sex
            if isinstance(birth, str):
                birth = datetime.strptime(birth, "%Y-%m-%d").date()
                birth = birth.strftime("%Y-%m-%d")
            elif isinstance(birth, list):
                birth = datetime.strptime(birth[0], "%Y-%m-%d").date()
                birth = birth.strftime("%Y-%m-%d")
            else:
                birth = None
            user.profile.birth = birth
            image = str(user.profile.image)
            user.profile.image = image.replace("frontend", "")
            user.profile.save()

        if data.get("password") is not None:
            user.set_password(data["password"])
        user.save()
        if user:
            return Response(
                self.serializer_class(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
