from django.conf import settings
from django.db import models


class Company(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_companies"
    )
    name = models.CharField(max_length=150)
    logo = models.ImageField(
        upload_to="companies/logos/",
        blank=True,
        null=True
    )
    description = models.TextField()
    website = models.URLField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=150)
    industry = models.CharField(max_length=100)
    employee_count = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    founded_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    