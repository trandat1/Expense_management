from .views import index
from django.urls import path,include

urlpatterns = [
    path("",index),
    # path("api/",include("api.urls")),
    # path("/",include("frontend.urls"))
]
