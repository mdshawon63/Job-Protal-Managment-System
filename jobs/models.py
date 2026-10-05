from django.conf import settings
from django.db import models


class Job(models.Model):

    class JobType(models.TextChoices):
        FULL_TIME = "full_time", "Full Time"
        PART_TIME = "part_time", "Part Time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"
        REMOTE = "remote", "Remote"

    class ExperienceLevel(models.TextChoices):
        ENTRY = "entry", "Entry Level"
        MID = "mid", "Mid Level"
        SENIOR = "senior", "Senior Level"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()

    location = models.CharField(max_length=150)

    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
        default=JobType.FULL_TIME
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.ENTRY
    )

    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    skills = models.TextField()

    application_deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class JobBookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_bookmarks"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "job"],
                name="unique_job_bookmark"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"