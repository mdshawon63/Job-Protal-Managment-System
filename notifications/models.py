from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        APPLICATION = "application", "Application"
        STATUS_UPDATE = "status_update", "Status Update"
        INTERVIEW = "interview", "Interview"
        SYSTEM = "system", "System"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"