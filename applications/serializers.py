from django.utils import timezone

from rest_framework import serializers

from .models import Application, Interview


MAX_RESUME_SIZE = 5 * 1024 * 1024

ALLOWED_RESUME_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
]


class ApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="job.company.name",
        read_only=True
    )

    candidate_name = serializers.CharField(
        source="candidate.username",
        read_only=True
    )

    class Meta:
        model = Application

        fields = [
            "id",
            "job",
            "job_title",
            "company_name",
            "candidate",
            "candidate_name",
            "cover_letter",
            "resume",
            "status",
            "recruiter_note",
            "applied_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "candidate_name",
            "status",
            "recruiter_note",
            "applied_at",
            "updated_at",
        ]

    def validate_resume(self, value):

        if value.size > MAX_RESUME_SIZE:

            raise serializers.ValidationError(
                "Resume file size cannot exceed 5 MB."
            )

        extension = ""

        if "." in value.name:

            extension = (
                "."
                + value.name.rsplit(".", 1)[1].lower()
            )

        if extension not in ALLOWED_RESUME_EXTENSIONS:

            raise serializers.ValidationError(
                "Only PDF, DOC and DOCX files are allowed."
            )

        return value

    def validate(self, attrs):

        request = self.context.get("request")

        job = attrs.get("job")

        if job:

            if job.status != "published":

                raise serializers.ValidationError({
                    "job": "You can only apply to published jobs."
                })

            if (
                job.application_deadline
                and job.application_deadline
                < timezone.now()
            ):

                raise serializers.ValidationError({
                    "job": "The application deadline has passed."
                })

            if request:

                candidate = request.user

                if Application.objects.filter(
                    job=job,
                    candidate=candidate
                ).exists():

                    raise serializers.ValidationError({
                        "job": (
                            "You have already applied "
                            "to this job."
                        )
                    })

        return attrs


class ApplicationStatusSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Application

        fields = [
            "status",
            "recruiter_note",
            "updated_at",
        ]

        read_only_fields = [
            "updated_at",
        ]


class InterviewSerializer(
    serializers.ModelSerializer
):

    candidate_name = serializers.CharField(
        source="application.candidate.username",
        read_only=True
    )

    job_title = serializers.CharField(
        source="application.job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="application.job.company.name",
        read_only=True
    )

    class Meta:
        model = Interview

        fields = [
            "id",
            "application",
            "candidate_name",
            "job_title",
            "company_name",
            "scheduled_at",
            "interview_type",
            "meeting_link",
            "location",
            "status",
            "recruiter_note",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate_name",
            "job_title",
            "company_name",
            "created_at",
            "updated_at",
        ]


class RecruiterApplicationAnalyticsSerializer(
    serializers.Serializer
):

    total_applications = serializers.IntegerField()

    applied = serializers.IntegerField()
    reviewing = serializers.IntegerField()
    shortlisted = serializers.IntegerField()
    interview = serializers.IntegerField()
    selected = serializers.IntegerField()
    rejected = serializers.IntegerField()
    withdrawn = serializers.IntegerField()

    selection_rate = serializers.FloatField()
    rejection_rate = serializers.FloatField()


class JobApplicationAnalyticsSerializer(
    serializers.Serializer
):

    job_id = serializers.IntegerField()
    job_title = serializers.CharField()

    total_applications = serializers.IntegerField()

    applied = serializers.IntegerField()
    reviewing = serializers.IntegerField()
    shortlisted = serializers.IntegerField()
    interview = serializers.IntegerField()
    selected = serializers.IntegerField()
    rejected = serializers.IntegerField()
    withdrawn = serializers.IntegerField()