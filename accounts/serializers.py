from rest_framework import serializers

from .models import (
    User,
    CandidateProfile,
    RecruiterProfile,
)


MAX_RESUME_SIZE = 5 * 1024 * 1024
MAX_PROFILE_PICTURE_SIZE = 2 * 1024 * 1024

ALLOWED_RESUME_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
]

ALLOWED_PROFILE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "role",
        ]

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():

            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user


class CandidateProfileSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = CandidateProfile

        fields = [
            "id",
            "full_name",
            "date_of_birth",
            "location",
            "bio",
            "skills",
            "education",
            "experience",
            "resume",
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


class RecruiterProfileSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = RecruiterProfile

        fields = [
            "id",
            "full_name",
            "designation",
            "bio",
        ]


class CandidateDashboardSerializer(
    serializers.Serializer
):

    total_applications = serializers.IntegerField()
    applied = serializers.IntegerField()
    reviewing = serializers.IntegerField()
    shortlisted = serializers.IntegerField()
    interviews = serializers.IntegerField()
    selected = serializers.IntegerField()
    rejected = serializers.IntegerField()
    saved_jobs = serializers.IntegerField()
    upcoming_interviews = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()


class RecruiterDashboardSerializer(
    serializers.Serializer
):

    total_jobs = serializers.IntegerField()
    published_jobs = serializers.IntegerField()
    draft_jobs = serializers.IntegerField()
    closed_jobs = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    reviewing_applications = serializers.IntegerField()
    shortlisted_applications = serializers.IntegerField()
    interview_applications = serializers.IntegerField()
    selected_applications = serializers.IntegerField()
    rejected_applications = serializers.IntegerField()
    upcoming_interviews = serializers.IntegerField()