from django.contrib.auth import logout
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
# Models
from .forms import CustomLoginForm, CustomRegisterForm
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

        if self.request.user.role == CustomUser.REVIEWER:
            return render(request, "users/redactor-profile.html", context)

        return render(request, "users/profile.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')  # или твой путь для редиректа после выхода

    login_url = '/users/login/'
    return HttpResponseForbidden()  # Отказ от доступа для GET-запроса


def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Блокируем до активации
            user.save()

            # Генерация ссылки активации
            current_site = get_current_site(request)
            subject = 'Активация аккаунта'
            message = render_to_string('email/activation_email.html',
    {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(
                subject,
                message,
                "e.bahytzhanuly@tau-edu.kz",
                [user.email],
            )

            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'email/activation_success.html')
    else:
        return render(request, 'email/activation_invalid.html')