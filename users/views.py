from django.contrib.auth import logout
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView

# Models
from .forms import CustomLoginForm
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile.html"
    login_url = '/users/login/'

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if self.request.user.role == CustomUser.REDACTOR:
            return render(request, "users/redactor-profile.html", context)
        return render(request, "users/profile.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')  # или твой путь для редиректа после выхода

    login_url = '/users/login/'
    return HttpResponseForbidden()  # Отказ от доступа для GET-запроса
