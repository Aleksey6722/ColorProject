from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
import re

re_email = re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d-]+(\.[A-Z|a-z]{2,})+')

def index(request):
    return render(request, 'core/index.html')


def sign_in(request):
    return render(request, 'core/enter-form.html')


def sign_up(request):
    return render(request, 'core/registration-form.html')


def find_car(request):
    return HttpResponse('find_car')


def api_sign_up(request):
    data = json.loads(request.body.decode())

    login = data.get('login')
    password = data.get('password')
    password2 = data.get('password2')
    email = data.get('email')
    name = data.get('name')
    hashed_password = hashlib.sha256(password.encode())
    hexpassword = hashed_password.hexdigest()

    if re.fullmatch(re_email, email) is None:
        return JsonResponse(data={'error': 'Введён некорректный email'}, status=400)

    if password != password2:
        return JsonResponse(data={'error': 'Пароли не совпадают'}, status=400)

    # try:
    #     user = User.query.filter_by(login=login).scalar()
    #     if user is not None:
    #         return jsonify({'error': 'Такой логин уже используется'}), 400
    #     email_check = User.query.filter_by(email=email).scalar()
    #     if email_check is not None:
    #         return jsonify({'error': 'Такой email уже существует'}), 400
    #     user = User(login=login, name=name, password=hexpassword, email=email)
    #     db.session.add(user)
    #     db.session.commit()
    #     a_dict = {'login': user.login, 'name': user.name, 'email': user.email,
    #               'registration_date': user.registration_date}
    # except BaseException as e:
    #     print(e)
    #     return jsonify({'error': f'Неизвестная ошибка'}), 400

    return JsonResponse(data={'info': 'come info'}, status=200)




def api_sign_in(request):
    return JsonResponse({'error': 'api_sign_in'})


def fav(request):
    return HttpResponse('fav')

