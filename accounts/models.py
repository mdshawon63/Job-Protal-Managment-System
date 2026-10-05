from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        CANDIDATE = "candidate", "Candidate"
        RECRUITER = "recruiter", "Recruiter"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE
    )
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="candidate_profile"
    )
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="recruiter_profile"
    )
    full_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name