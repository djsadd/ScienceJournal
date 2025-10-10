# app/mixins.py
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from bid.models import Bid, BidStatus


class BidAccessMixin:
    """
    Миксин для проверки опубликованности статьи.
    Использует bid_pk из URL.
    """

    def get_bid(self):
        """Удобный метод для получения заявки (Bid)"""
        bid_pk = self.kwargs['bid_pk']
        return Bid.objects.get(pk=bid_pk)

    def dispatch(self, request, *args, **kwargs):
        bid = self.get_bid()

        # 🔒 Здесь твоя логика проверки
        # Например, только автор заявки или редактор
        if bid.status==BidStatus.PUBLISHED:
            messages.error(request, "Данная статья уже опубликована")
            return redirect("edit-request-redactor", bid.pk)

        # Сохраняем заявку, чтобы не загружать её дважды
        self.bid = bid

        return super().dispatch(request, *args, **kwargs)


class BidAccessMixinPOST:
    """
    Миксин для проверки опубликованности статьи.
    Использует bid_pk из URL.
    """

    def get_bid(self):
        """Удобный метод для получения заявки (Bid)"""
        bid_pk = self.kwargs['bid_pk']
        return Bid.objects.get(pk=bid_pk)

    def dispatch(self, request, *args, **kwargs):
        bid = self.get_bid()

        # 🔒 Здесь твоя логика проверки
        # Например, только автор заявки или редактор
        if request.method=="POST" and BidStatus.status==BidStatus.PUBLISHED:
            messages.error(request, "Данная статья уже опубликована")
            return redirect("edit-request-redactor", bid.pk)

        # Сохраняем заявку, чтобы не загружать её дважды
        self.bid = bid

        return super().dispatch(request, *args, **kwargs)
