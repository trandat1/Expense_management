from .views import UsersView,CreateUserView
from django.urls import path,include

urlpatterns = [
    path("",UsersView.as_view()),
    path("create",CreateUserView.as_view()),
    # path("api/",include("api.urls")),
    # path("/",include("frontend.urls"))
]
