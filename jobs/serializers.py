from rest_framework import serializers

from .models import Job, JobBookmark


class JobSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "company",
            "company_name",
            "posted_by",
            "title",
            "description",
            "requirements",
            "responsibilities",
            "location",
            "job_type",
            "experience_level",
            "salary_min",
            "salary_max",
            "skills",
            "application_deadline",
            "status",
            "is_featured",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "posted_by",
            "company_name",
            "created_at",
            "updated_at",
        ]

    def validate_company(self, company):

        user = self.context["request"].user

        if user.role == "admin":
            return company

        if company.owner != user:
            raise serializers.ValidationError(
                "You can only create jobs for your own company."
            )

        return company


class JobBookmarkSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="job.company.name",
        read_only=True
    )

    class Meta:
        model = JobBookmark

        fields = [
            "id",
            "job",
            "job_title",
            "company_name",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]