from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        fields = [
            "id",
            "name",
            "logo",
            "description",
            "website",
            "email",
            "phone",
            "location",
            "industry",
            "employee_count",
            "founded_year",
            "is_verified",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class CompanyVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        fields = [
            "id",
            "name",
            "is_verified",
        ]

        read_only_fields = [
            "id",
            "name",
        ]