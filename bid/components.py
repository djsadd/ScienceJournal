from .models import BidStatus


def send_to_recent(request, obj):
    if obj.review:
        obj.status = BidStatus.RE_REVIEW
        obj.save()
        return obj

    obj.status = BidStatus.SENT_FOR_REVIEW
    obj.save()
    return obj
