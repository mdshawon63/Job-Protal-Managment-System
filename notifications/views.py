from rest_framework import generics
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        )


class UnreadNotificationListView(generics.ListAPIView):

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        )


class NotificationReadView(generics.UpdateAPIView):

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(is_read=True)


class MarkAllNotificationsReadView(
    generics.UpdateAPIView
):

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        )

    def update(self, request, *args, **kwargs):

        self.get_queryset().update(is_read=True)

        return Response(
            {
                "message": "All notifications marked as read."
            }
        )