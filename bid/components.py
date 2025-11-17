from .models import BidStatus, Review
from users.models import CustomUser
from components.tasks import send_mail_task

from django.conf import settings


def send_to_recent(request, obj):

    reviewer = CustomUser.objects.get(role=CustomUser.REVIEWER)

    if Review.objects.filter(bid=obj, reviewer=request.user):
        obj.status = BidStatus.RE_REVIEW
        obj.save()
        print("SEND")

        send_mail_task.delay(
            "Review moved back for re-review",
            "A bid has returned to the re-review queue.",
            settings.DEFAULT_FROM_EMAIL,
            ['e.bahytzhanuly@tau-edu.kz'],
            fail_silently=False,
        )
        return obj

    review_obj = Review.objects.create(
        bid=obj,
        reviewer=reviewer,
    )
    review_obj.save()

    obj.status = BidStatus.SENT_FOR_REVIEW
    obj.save()
    print("SEND")
    send_mail_task.delay(
        "New review assignment",
        "A reviewer has been assigned to a bid.",
        settings.DEFAULT_FROM_EMAIL,
        ['e.bahytzhanuly@tau-edu.kz'],
        fail_silently=False,
    )
    return obj

