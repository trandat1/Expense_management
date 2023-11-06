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
        data = request.data
        if serializer.is_valid():
            profile_data = {}
            for key in ["profile.sex", "profile.birth", "profile.image"]:
                profile_data[key.split(".")[1]] = request.data.pop(key, None)
            image = profile_data.get("image", None)
            sex = profile_data.get("sex", None)
            birth = profile_data.get("birth", None)
            user = User(email=data["email"], username=data["username"])
            user.set_password(data["password"])
            user.save()
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
    serializer_class = UserSerializer
    def get(self, request, id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_id = id
        user_data = User.objects.get(id=user_id)
        if user_data:
            return Response(
                self.serializer_class(user_data).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    permission_classes = [IsAuthenticated]
    def put(self, request, id, *args, **kwargs):
        user_id = id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        profile_data = {}
        for key in ["profile.sex", "profile.birth", "profile.image"]:
            profile_data[key.split(".")[1]] = data.pop(key, None)

        image = profile_data.get("image", None)
        sex = profile_data.get("sex", None)
        birth = profile_data.get("birth", None)

        user.set_password(data["password"])
        user.save()

        if image is not None:
            user.profile.image = image[0] if isinstance(image, list) else image
        if sex is not None:
            user.profile.sex = sex[0] if isinstance(sex, list) else sex
        if birth is not None:
            if isinstance(birth, str):
                birth = datetime.fromisoformat(birth).date()
            elif isinstance(birth, list):
                birth = datetime.fromisoformat(birth[0]).date()
            else:
                birth = None
            user.profile.birth = birth

        if image is not None:
            image = str(user.profile.image)
            user.profile.image = image.replace("frontend", "")
        
        user.profile.save()

        return Response(
            self.serializer_class(user).data, status=status.HTTP_200_OK
        )
