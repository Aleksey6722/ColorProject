from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from .forms import RegForm, AuthForm
from .models import Session, Car, Favourite
from .serializers import UserSerializer, ColorSerializer, CarIDSerializer, FavoriteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework.decorators import api_view, permission_classes
from .colors import calculation
import hashlib
import time


@permission_classes([permissions.AllowAny])
def find_cars(request):
    return render(request, 'core/picker.html')


@permission_classes([permissions.AllowAny])
def index(request):
    return render(request, 'core/index.html')


@permission_classes([permissions.AllowAny])
def sign_in(request):
    form = AuthForm()
    return render(request, 'core/authorization-form.html', context={'form': form})


@permission_classes([permissions.AllowAny])
def sign_up(request):
    form = RegForm()
    return render(request, 'core/registration-form.html', context={'form': form})


@permission_classes([permissions.IsAuthenticated])
def sign_out(request):
    response = HttpResponseRedirect('/')
    response.headers['Authorization'] = None
    return response


@permission_classes([permissions.AllowAny])
def about(request):
    return render(request, 'core/about.html')


class APIFindCars(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = ColorSerializer(data={'color': request.GET.get('c').upper(), 'n': request.GET.get('n')})
        serializer.is_valid(raise_exception=True)

        n = serializer.data['n']
        input_color = serializer.data['color']

        data = Car.objects.all()
        a_list = []
        for car in data:
            id = car.pk
            car_color = car.color.color_name
            model = car.model
            brand = car.brand.name
            url = car.image.url
            country = car.brand.country.name
            elem = id, model, brand, car_color, calculation(input_color, car_color), url, country
            a_list.append(elem)

        if n > len(a_list):
            n=len(a_list)

        sorted_list = sorted(a_list, key=lambda i: i[4])[:n]

        result = []
        for x in sorted_list:
            car_info = {
                        'id': x[0],
                        'model': x[1],
                        'brand': x[2],
                        'color': x[3],
                        'url': x[5],
                        'country': x[6]
                        }
            result.append(car_info)

        return Response(result)


class APIFavorite(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    User = get_user_model()

    def post(self, request):
        serializer = CarIDSerializer(data={'car_id': request.data['car_id']})
        serializer.is_valid(raise_exception=True)
        car_id = serializer.data['car_id']
        car = Car.objects.filter(pk=car_id).first()
        user = User.objects.filter(pk=sess.user.pk).first()
        fav = Favourite.objects.filter(user=user, car=car)
        if fav:
            return Response({'error': 'Уже в избранном'}, status=400)
        fav = Favourite(user=user, car=car)
        fav.save()
        return Response(FavoriteSerializer(fav).data)

    def delete(self, request):
        serializer = CarIDSerializer(data={'car_id': request.data['car_id']})
        serializer.is_valid(raise_exception=True)
        car_id = serializer.data['car_id']
        car = Car.objects.filter(pk=car_id).first()
        user = User.objects.filter(pk=sess.user.pk).first()
        fav = Favourite.objects.filter(user=user, car=car)
        if not fav:
            return Response({'error': 'Отсутствует в избранном'}, status=400)
        fav.delete()
        return Response({'success': 'Успешно удалено из избранного'})


class Fav(View):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        User = get_user_model()
        user = User.objects.get(auth_token=token)
        if not user:
            return render(request, 'core/fav_unauth.html')
        carset = Favourite.objects.filter(user=user)
        return render(request, 'core/favourite.html', context={'carset': carset, 'user': user})
