from django.db.models import Q

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import (
    IsCandidate,
    IsRecruiterOrAdmin,
)

from .models import Job, JobBookmark
from .serializers import (
    JobSerializer,
    JobBookmarkSerializer,
)


class JobPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class JobListCreateView(generics.ListCreateAPIView):

    serializer_class = JobSerializer
    pagination_class = JobPagination

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsRecruiterOrAdmin()]

        return [IsCandidate()]

    def get_queryset(self):

        if self.request.user.role == "candidate":

            queryset = Job.objects.filter(
                status=Job.Status.PUBLISHED
            ).select_related("company")

        elif self.request.user.role == "admin":

            queryset = Job.objects.all().select_related(
                "company"
            )

        else:

            queryset = Job.objects.filter(
                posted_by=self.request.user
            ).select_related("company")

        search = self.request.query_params.get(
            "search"
        )

        location = self.request.query_params.get(
            "location"
        )

        job_type = self.request.query_params.get(
            "job_type"
        )

        experience = self.request.query_params.get(
            "experience_level"
        )

        min_salary = self.request.query_params.get(
            "min_salary"
        )

        max_salary = self.request.query_params.get(
            "max_salary"
        )

        ordering = self.request.query_params.get(
            "ordering"
        )

        if search:

            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(requirements__icontains=search)
                | Q(responsibilities__icontains=search)
                | Q(skills__icontains=search)
                | Q(company__name__icontains=search)
            )

        if location:

            queryset = queryset.filter(
                location__icontains=location
            )

        if job_type:

            queryset = queryset.filter(
                job_type=job_type
            )

        if experience:

            queryset = queryset.filter(
                experience_level=experience
            )

        if min_salary:

            try:

                queryset = queryset.filter(
                    salary_max__gte=float(min_salary)
                )

            except ValueError:
                pass

        if max_salary:

            try:

                queryset = queryset.filter(
                    salary_min__lte=float(max_salary)
                )

            except ValueError:
                pass

        if ordering == "oldest":

            queryset = queryset.order_by(
                "created_at"
            )

        elif ordering == "salary_high":

            queryset = queryset.order_by(
                "-salary_max"
            )

        elif ordering == "salary_low":

            queryset = queryset.order_by(
                "salary_min"
            )

        else:

            queryset = queryset.order_by(
                "-created_at"
            )

        return queryset

    def perform_create(self, serializer):

        serializer.save(
            posted_by=self.request.user
        )


class JobDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = JobSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsCandidate()]

        return [IsRecruiterOrAdmin()]

    def get_queryset(self):

        if self.request.user.role == "candidate":

            return Job.objects.filter(
                status=Job.Status.PUBLISHED
            ).select_related("company")

        if self.request.user.role == "admin":

            return Job.objects.all().select_related(
                "company"
            )

        return Job.objects.filter(
            posted_by=self.request.user
        ).select_related("company")


class JobBookmarkListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = JobBookmarkSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):

        return JobBookmark.objects.filter(
            user=self.request.user
        ).select_related(
            "job",
            "job__company"
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


class JobBookmarkDeleteView(
    generics.DestroyAPIView
):

    serializer_class = JobBookmarkSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):

        return JobBookmark.objects.filter(
            user=self.request.user
        )