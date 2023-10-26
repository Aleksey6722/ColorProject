from django.urls import path

from .views import APISignIn, APISignUp, APIFindCars, APIFavorite

urlpatterns = [
    path("signin", APISignIn.as_view(), name="api_sign_in"),
    path("signup", APISignUp.as_view(), name="api_sign_up"),
    path("fav", APIFavorite.as_view(), name="fav"),
    path("find-cars", APIFindCars.as_view(), name="api_find_cars"),
]
