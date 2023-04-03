from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from .forms import RegForm, AuthForm
from .models import User, Session, Car, Favourite
from .serializers import UserSerializer, ColorSerializer, CarIDSerializer, FavoriteSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .colors import calculation
import json
import hashlib
import re
import time


def test(request):
    return render(request, 'core/picker.html')

def index(request):
    return render(request, 'core/index.html')


def sign_in(request):
    form = AuthForm()
    return render(request, 'core/authorization-form.html', context={'form': form})


def sign_up(request):
    form = RegForm()
    return render(request, 'core/registration-form.html', context={'form': form})


def find_car(request):
    return HttpResponse('find_car')


class APISignUp(APIView):
    def post(self, request):
        form = RegForm(request.data)
        if form.is_valid():
            form.save()
            user = User.objects.values('login', 'name', 'email', 'registration_date',
                                       'last_signin_date').filter(email=form.cleaned_data['email']).first()
            return Response({'user': UserSerializer(user).data})

        return Response(form.errors.get_json_data(), status=400)


class APISignIn(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        hashed_password = hashlib.sha256(password.encode())
        hexpassword = hashed_password.hexdigest()

        user = User.objects.all().filter(login=login).first()
        if user is None or user.password != hexpassword:
            return Response({'error': [{'message': 'Неверный логин или пароль'}]}, status=403)

        sess = Session(user=user)
        sess.save()
        user.last_signin_date = int(time.time())
        user.save()
        request.session['Authorization'] = sess.key
        return Response({'id': user.pk, 'login': user.login, 'name': user.name, 'email': user.email})


class APIFindCars(APIView):
    def get(self, request):
        serializer = ColorSerializer(data={'color': request.GET.get('c').upper(), 'n': request.GET.get('n')})
        serializer.is_valid(raise_exception=True)

        n = serializer.data['n']
        input_color = serializer.data['color']

        data = Car.objects.all()
        a_list = []
        for car in data:
            car_color = car.color.color_name
            model = car.model
            brand = car.brand.name
            elem = model, brand, car_color, calculation(input_color, car_color)
            a_list.append(elem)

        sorted_list = sorted(a_list, key=lambda i: i[3])[:n]

        result = []
        for x in sorted_list:
            car_info = {'model': x[0], 'brand': x[1], 'color': x[2]}
            result.append(car_info)

        return Response(result)


class APIFavorite(APIView):

    def post(self, request):
        key = request.session.get('Authorization')
        sess = Session.objects.filter(key=key).first()
        if not sess:
            return Response({'error': 'Нужна авторизация'}, status=401)
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
        key = request.session.get('Authorization')
        sess = Session.objects.filter(key=key).first()
        if not sess:
            return Response({'error': 'Нужна авторизация'}, status=401)
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

