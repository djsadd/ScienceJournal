from .models import BidStatus, Review
from users.models import CustomUser
from django.core.mail import send_mail

from django.conf import settings


def send_to_recent(request, obj):

    # user test in future he func to change
    user = CustomUser.objects.get(role=CustomUser.REVIEWER)

    if Review.objects.filter(bid=obj, reviewer=request.user):
        obj.status = BidStatus.RE_REVIEW
        obj.save()
        print("SEND")

        send_mail(
            'Успешно отправили статью на рецензирование',
            'Текст письма',
            settings.DEFAULT_FROM_EMAIL,
            ['e.bahytzhanuly@tau-edu.kz'],
            fail_silently=False,
        )
        return obj

    review_obj = Review.objects.create()
    review_obj.bid = obj
    review_obj.reviewer = user
    review_obj.save()

    obj.status = BidStatus.SENT_FOR_REVIEW
    obj.save()
    print("SEND")
    send_mail(
        'Успешно отправили статью на рецензирование',
        'Текст письма',
        settings.DEFAULT_FROM_EMAIL,
        ['e.bahytzhanuly@tau-edu.kz'],
        fail_silently=False,
    )
    return obj
