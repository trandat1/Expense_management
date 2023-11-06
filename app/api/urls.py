from .views import UsersView,CreateUserView,UpdateUserView
from django.urls import path,include

urlpatterns = [
    path("",UsersView.as_view()),
    path("create_user",CreateUserView.as_view()),
    path("update_user/<str:id>",UpdateUserView.as_view()),
    # path("/",include("frontend.urls"))
]
