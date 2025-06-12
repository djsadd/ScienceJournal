from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from users.models import CustomUser


class ReviewRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role != CustomUser.REVIEWER:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)
