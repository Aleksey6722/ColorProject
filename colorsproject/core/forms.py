from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

import re
import hashlib

from django import forms
from .models import User

re_email = re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d-]+(\.[A-Z|a-z]{2,})+')
re_login = re.compile(r'^[a-zA-Z][a-zA-Z0-9-_\.]{2,20}$')
re_password = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$')
re_name = re.compile(r'[A-Za-zА-Яа-яёЁ]*')  # [^a-zа-яё ]


class RegForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['login', 'name', 'email', 'password']
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form__input', 'placeholder': ' '}),
            'password': forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': ' ',
                                                   'id': 'password-input', 'name': 'password'}),
            'name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'class': 'form__input', 'placeholder': ' '})
        }

    error_messages = {
        'email_invalid': 'Введите корректный email',
        'email_unique': 'Такой Email уже существует',
        'password_invalid': 'Пароль должен содержать строчные и прописные латинские буквы, цифры. '
                          'Минимум 6 символов',
        'login_invalid': 'Введите корректный логин, минимум 3 символа на латинице',
        'login_unique': 'Такой логин уже существует',
        'name_invalid': 'Введите корректное имя'
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        if re.fullmatch(re_email, email) is None:
            raise ValidationError(self.error_messages['email_invalid'])
        try:
            User.objects.get(email=email)
            raise ValidationError(self.error_messages['email_unique'])
        except User.DoesNotExist:
            return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if re.fullmatch(re_password, password) is None:
            raise ValidationError(self.error_messages['password_invalid'])
        hashed_password = hashlib.sha256(password.encode())
        hexpassword = hashed_password.hexdigest()
        return hexpassword

    def clean_login(self):
        login = self.cleaned_data['login']
        if re.fullmatch(re_login, login) is None:
            raise ValidationError(self.error_messages['login_invalid'])
        try:
            User.objects.get(login=login)
            raise ValidationError(self.error_messages['login_unique'])
        except User.DoesNotExist:
            return login

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.fullmatch(re_name, name) is None:
            raise ValidationError(self.error_messages['name_invalid'])
        return name


class AuthForm(forms.Form):
    login = forms.CharField(max_length=20, required=True, label='Логин',
                            widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': ' ',
                                                               'id': 'login-input'})
                            )
    password = forms.CharField(max_length=64, required=True, label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': ' ',
                                                                 'id': 'password-input'})
                               )


