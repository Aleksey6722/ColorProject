from django.urls import path

from .views import api_sign_in, api_sign_up, find_car, fav


urlpatterns = [
    path("signin", api_sign_in, name="api_sign_in"),
    path("signup", api_sign_up, name="api_sign_up"),
    path("fav", fav, name="fav"),
    path("find-car", find_car, name="find_car"),
]
