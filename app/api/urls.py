from .views import UsersView,CreateUserView,UpdateUserView, HistoriesUserView, Create_Histories_User
from django.urls import path,include

urlpatterns = [
    path("",UsersView.as_view()),
    path("create_user",CreateUserView.as_view()),
    path("update_user/<str:id>",UpdateUserView.as_view()),
    path('users/<str:user_id>/histories/', HistoriesUserView.as_view(), name='user-histories'),
    path('users/<str:user_id>/histories/create', Create_Histories_User.as_view(), name='user-create-histories'),
    # path("/",include("frontend.urls"))
]
