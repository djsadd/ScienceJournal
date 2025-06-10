from .models import BidStatus, Review
from users.models import CustomUser


def send_to_recent(request, obj):

    # user test in future he func to change
    user = CustomUser.objects.get(role=CustomUser.REVIEWER)

    if Review.objects.filter(bid=obj, reviewer=request.user):
        obj.status = BidStatus.RE_REVIEW
        obj.save()
        return obj

    review_obj = Review.objects.create()
    review_obj.bid = obj
    review_obj.reviewer = user
    review_obj.save()

    obj.status = BidStatus.SENT_FOR_REVIEW
    obj.save()
    return obj
