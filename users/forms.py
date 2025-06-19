from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


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


class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="Имя", required=True)
    last_name = forms.CharField(max_length=30, label="Фамилия", required=True)
    email = forms.EmailField(label="Электронная почта", required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user