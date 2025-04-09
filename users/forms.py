from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'id': 'username',
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
            'required': True
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль',
            'required': True
        })
    )
