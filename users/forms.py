from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Имя пользователя или email'),
        widget=forms.TextInput(attrs={
            'id': 'username',
            'class': 'form-control',
            'placeholder': _('Введите имя пользователя или email'),
            'required': True
        })
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'placeholder': _('Введите пароль'),
            'required': True
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        if username and '@' in username:
            try:
                user = CustomUser.objects.get(email__iexact=username)
                self.cleaned_data['username'] = user.get_username()
            except CustomUser.DoesNotExist:
                pass
        return super().clean()


class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label=_("Имя"), required=True)
    last_name = forms.CharField(max_length=30, label=_("Фамилия"), required=True)
    email = forms.EmailField(label=_("Электронная почта"), required=True)

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
