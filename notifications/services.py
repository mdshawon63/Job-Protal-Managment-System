from .models import Notification


def create_notification(
    recipient,
    title,
    message,
    notification_type
):
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
    )