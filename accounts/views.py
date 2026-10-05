from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application, Interview
from jobs.models import Job, JobBookmark
from notifications.models import Notification

from .models import User, CandidateProfile, RecruiterProfile
from .permissions import IsCandidate, IsRecruiter
from .serializers import (
    RegisterSerializer,
    CandidateProfileSerializer,
    RecruiterProfileSerializer,
    CandidateDashboardSerializer,
    RecruiterDashboardSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CandidateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsCandidate]

    def get_object(self):
        profile, created = CandidateProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                "full_name": self.request.user.get_full_name()
                or self.request.user.username
            }
        )
        return profile


class RecruiterProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsRecruiter]

    def get_object(self):
        profile, created = RecruiterProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                "full_name": self.request.user.get_full_name()
                or self.request.user.username
            }
        )
        return profile


class CandidateDashboardView(APIView):
    permission_classes = [IsCandidate]
    serializer_class = CandidateDashboardSerializer

    def get(self, request):
        user = request.user

        applications = Application.objects.filter(
            candidate=user
        )

        upcoming_interviews = Interview.objects.filter(
            application__candidate=user,
            scheduled_at__gte=timezone.now(),
            status=Interview.Status.SCHEDULED
        )

        data = {
            "total_applications": applications.count(),
            "applied": applications.filter(
                status=Application.Status.APPLIED
            ).count(),
            "reviewing": applications.filter(
                status=Application.Status.REVIEWING
            ).count(),
            "shortlisted": applications.filter(
                status=Application.Status.SHORTLISTED
            ).count(),
            "interviews": applications.filter(
                status=Application.Status.INTERVIEW
            ).count(),
            "selected": applications.filter(
                status=Application.Status.SELECTED
            ).count(),
            "rejected": applications.filter(
                status=Application.Status.REJECTED
            ).count(),
            "saved_jobs": JobBookmark.objects.filter(
                user=user
            ).count(),
            "upcoming_interviews": upcoming_interviews.count(),
            "unread_notifications": Notification.objects.filter(
                recipient=user,
                is_read=False
            ).count(),
        }

        serializer = CandidateDashboardSerializer(data)

        return Response(serializer.data)


class RecruiterDashboardView(APIView):
    permission_classes = [IsRecruiter]
    serializer_class = RecruiterDashboardSerializer

    def get(self, request):
        user = request.user

        jobs = Job.objects.filter(
            posted_by=user
        )

        applications = Application.objects.filter(
            job__posted_by=user
        )

        upcoming_interviews = Interview.objects.filter(
            application__job__posted_by=user,
            scheduled_at__gte=timezone.now(),
            status=Interview.Status.SCHEDULED
        )

        data = {
            "total_jobs": jobs.count(),
            "published_jobs": jobs.filter(
                status=Job.Status.PUBLISHED
            ).count(),
            "draft_jobs": jobs.filter(
                status=Job.Status.DRAFT
            ).count(),
            "closed_jobs": jobs.filter(
                status=Job.Status.CLOSED
            ).count(),
            "total_applications": applications.count(),
            "reviewing_applications": applications.filter(
                status=Application.Status.REVIEWING
            ).count(),
            "shortlisted_applications": applications.filter(
                status=Application.Status.SHORTLISTED
            ).count(),
            "interview_applications": applications.filter(
                status=Application.Status.INTERVIEW
            ).count(),
            "selected_applications": applications.filter(
                status=Application.Status.SELECTED
            ).count(),
            "rejected_applications": applications.filter(
                status=Application.Status.REJECTED
            ).count(),
            "upcoming_interviews": upcoming_interviews.count(),
        }

        serializer = RecruiterDashboardSerializer(data)

        return Response(serializer.data)