from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from users.models import CustomUser


class BidAccessPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        self.object = self.get_object()

        if (
            request.user.role in [CustomUser.REDACTOR, CustomUser.REVIEWER]
            or self.object.responsible == request.user
        ):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied()
