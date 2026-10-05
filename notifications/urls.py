from django.urls import path

from .views import (
    NotificationListView,
    UnreadNotificationListView,
    NotificationReadView,
    MarkAllNotificationsReadView,
)


urlpatterns = [
    path(
        "",
        NotificationListView.as_view(),
        name="notification-list"
    ),

    path(
        "unread/",
        UnreadNotificationListView.as_view(),
        name="notification-unread"
    ),

    path(
        "<int:pk>/read/",
        NotificationReadView.as_view(),
        name="notification-read"
    ),

    path(
        "read-all/",
        MarkAllNotificationsReadView.as_view(),
        name="notification-read-all"
    ),
]