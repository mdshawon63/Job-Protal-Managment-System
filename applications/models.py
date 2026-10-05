from django.conf import settings
from django.db import models


class Application(models.Model):

    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        REVIEWING = "reviewing", "Reviewing"
        SHORTLISTED = "shortlisted", "Shortlisted"
        INTERVIEW = "interview", "Interview"
        SELECTED = "selected", "Selected"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    cover_letter = models.TextField(blank=True)

    resume = models.FileField(
        upload_to="applications/resumes/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED
    )

    recruiter_note = models.TextField(blank=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["job", "candidate"],
                name="unique_job_application"
            )
        ]
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"
    
    
class Interview(models.Model):

    class InterviewType(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"
        PHONE = "phone", "Phone"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        RESCHEDULED = "rescheduled", "Rescheduled"

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    scheduled_at = models.DateTimeField()

    interview_type = models.CharField(
        max_length=20,
        choices=InterviewType.choices,
        default=InterviewType.ONLINE
    )

    meeting_link = models.URLField(
        blank=True
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )

    recruiter_note = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.application.candidate.username} - "
            f"{self.application.job.title}"
        )