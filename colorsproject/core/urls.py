from django.urls import path

from .views import APISignIn, APISignUp, APIFindCars, APIFavorite

urlpatterns = [
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
    path("fav", APIFavorite.as_view(), name="fav"),
    path("find-cars", APIFindCars.as_view(), name="api_find_cars"),
]
