from django.db.models import Count, Q

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCandidate
from notifications.services import create_notification

from .models import Application, Interview
from .permissions import IsJobRecruiter
from .serializers import (
    ApplicationSerializer,
    ApplicationStatusSerializer,
    InterviewSerializer,
    RecruiterApplicationAnalyticsSerializer,
    JobApplicationAnalyticsSerializer,
)


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(
            candidate=self.request.user
        ).select_related(
            "job",
            "job__company"
        )

    def perform_create(self, serializer):
        application = serializer.save(
            candidate=self.request.user
        )

        create_notification(
            recipient=application.job.posted_by,
            title="New Job Application",
            message=(
                f"{application.candidate.username} "
                f"applied for {application.job.title}."
            ),
            notification_type="application",
        )


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(
            candidate=self.request.user
        )


class RecruiterApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobRecruiter]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Application.objects.all().select_related(
                "job",
                "job__company",
                "candidate",
            )

        return Application.objects.filter(
            job__posted_by=self.request.user
        ).select_related(
            "job",
            "job__company",
            "candidate",
        )


class RecruiterApplicationUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsJobRecruiter]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Application.objects.all()

        return Application.objects.filter(
            job__posted_by=self.request.user
        )

    def perform_update(self, serializer):
        application = self.get_object()

        if application.status == "rejected":
            raise ValidationError(
                "A rejected application cannot be updated."
            )

        if application.status == "selected":
            raise ValidationError(
                "A selected application cannot be updated."
            )

        old_status = application.status
        updated_application = serializer.save()

        if old_status != updated_application.status:
            create_notification(
                recipient=updated_application.candidate,
                title="Application Status Updated",
                message=(
                    f"Your application for "
                    f"{updated_application.job.title} "
                    f"is now "
                    f"{updated_application.get_status_display()}."
                ),
                notification_type="status_update",
            )


class InterviewListCreateView(generics.ListCreateAPIView):
    serializer_class = InterviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsJobRecruiter()]

        return [IsCandidate()]

    def get_queryset(self):
        if self.request.user.role == "candidate":
            return Interview.objects.filter(
                application__candidate=self.request.user
            ).select_related(
                "application",
                "application__job",
                "application__job__company",
                "application__candidate",
            )

        if self.request.user.role == "admin":
            return Interview.objects.all().select_related(
                "application",
                "application__job",
                "application__job__company",
                "application__candidate",
            )

        return Interview.objects.filter(
            application__job__posted_by=self.request.user
        ).select_related(
            "application",
            "application__job",
            "application__job__company",
            "application__candidate",
        )

    def perform_create(self, serializer):
        application = serializer.validated_data["application"]

        if application.status != Application.Status.SHORTLISTED:
            raise ValidationError(
                "Interview can only be scheduled for shortlisted candidates."
            )

        if (
            self.request.user.role != "admin"
            and application.job.posted_by != self.request.user
        ):
            raise ValidationError(
                "You can only schedule interviews for your own jobs."
            )

        interview = serializer.save()

        create_notification(
            recipient=application.candidate,
            title="Interview Scheduled",
            message=(
                f"Your interview for "
                f"{application.job.title} "
                f"has been scheduled."
            ),
            notification_type="interview",
        )


class InterviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InterviewSerializer

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [IsCandidate()]

        if self.request.method == "GET":
            if self.request.user.role == "candidate":
                return [IsCandidate()]

            return [IsJobRecruiter()]

        return [IsJobRecruiter()]

    def get_queryset(self):
        if self.request.user.role == "candidate":
            return Interview.objects.filter(
                application__candidate=self.request.user
            )

        if self.request.user.role == "admin":
            return Interview.objects.all()

        return Interview.objects.filter(
            application__job__posted_by=self.request.user
        )

    def perform_update(self, serializer):
        old_status = self.get_object().status
        interview = serializer.save()

        if (
            old_status != interview.status
            and interview.status == "cancelled"
        ):
            create_notification(
                recipient=interview.application.candidate,
                title="Interview Cancelled",
                message=(
                    f"Your interview for "
                    f"{interview.application.job.title} "
                    f"has been cancelled."
                ),
                notification_type="interview",
            )


class RecruiterApplicationAnalyticsView(APIView):
    permission_classes = [IsJobRecruiter]
    serializer_class = RecruiterApplicationAnalyticsSerializer

    def get(self, request):
        if request.user.role == "admin":
            applications = Application.objects.all()
        else:
            applications = Application.objects.filter(
                job__posted_by=request.user
            )

        total = applications.count()

        applied = applications.filter(
            status=Application.Status.APPLIED
        ).count()

        reviewing = applications.filter(
            status=Application.Status.REVIEWING
        ).count()

        shortlisted = applications.filter(
            status=Application.Status.SHORTLISTED
        ).count()

        interview = applications.filter(
            status=Application.Status.INTERVIEW
        ).count()

        selected = applications.filter(
            status=Application.Status.SELECTED
        ).count()

        rejected = applications.filter(
            status=Application.Status.REJECTED
        ).count()

        withdrawn = applications.filter(
            status=Application.Status.WITHDRAWN
        ).count()

        selection_rate = (
            (selected / total) * 100
            if total
            else 0
        )

        rejection_rate = (
            (rejected / total) * 100
            if total
            else 0
        )

        data = {
            "total_applications": total,
            "applied": applied,
            "reviewing": reviewing,
            "shortlisted": shortlisted,
            "interview": interview,
            "selected": selected,
            "rejected": rejected,
            "withdrawn": withdrawn,
            "selection_rate": round(selection_rate, 2),
            "rejection_rate": round(rejection_rate, 2),
        }

        serializer = RecruiterApplicationAnalyticsSerializer(data)

        return Response(serializer.data)


class JobApplicationAnalyticsView(APIView):
    permission_classes = [IsJobRecruiter]
    serializer_class = JobApplicationAnalyticsSerializer

    def get(self, request):
        if request.user.role == "admin":
            queryset = Application.objects.all()
        else:
            queryset = Application.objects.filter(
                job__posted_by=request.user
            )

        queryset = queryset.values(
            "job_id",
            "job__title"
        ).annotate(
            total_applications=Count("id"),
            applied=Count(
                "id",
                filter=Q(
                    status=Application.Status.APPLIED
                )
            ),
            reviewing=Count(
                "id",
                filter=Q(
                    status=Application.Status.REVIEWING
                )
            ),
            shortlisted=Count(
                "id",
                filter=Q(
                    status=Application.Status.SHORTLISTED
                )
            ),
            interview=Count(
                "id",
                filter=Q(
                    status=Application.Status.INTERVIEW
                )
            ),
            selected=Count(
                "id",
                filter=Q(
                    status=Application.Status.SELECTED
                )
            ),
            rejected=Count(
                "id",
                filter=Q(
                    status=Application.Status.REJECTED
                )
            ),
            withdrawn=Count(
                "id",
                filter=Q(
                    status=Application.Status.WITHDRAWN
                )
            )
        ).order_by(
            "-total_applications"
        )

        data = []

        for item in queryset:
            data.append({
                "job_id": item["job_id"],
                "job_title": item["job__title"],
                "total_applications": item["total_applications"],
                "applied": item["applied"],
                "reviewing": item["reviewing"],
                "shortlisted": item["shortlisted"],
                "interview": item["interview"],
                "selected": item["selected"],
                "rejected": item["rejected"],
                "withdrawn": item["withdrawn"],
            })

        serializer = JobApplicationAnalyticsSerializer(
            data,
            many=True
        )

        return Response(serializer.data)