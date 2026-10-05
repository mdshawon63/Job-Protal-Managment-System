from rest_framework import generics

from accounts.permissions import IsAdmin

from .models import Company
from .permissions import IsCompanyOwnerOrAdmin
from .serializers import (
    CompanySerializer,
    CompanyVerificationSerializer,
)


class CompanyListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = CompanySerializer
    permission_classes = [IsCompanyOwnerOrAdmin]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Company.objects.all()

        return Company.objects.filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            owner=self.request.user
        )


class CompanyDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = CompanySerializer
    permission_classes = [IsCompanyOwnerOrAdmin]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Company.objects.all()

        return Company.objects.filter(
            owner=self.request.user
        )


class CompanyVerificationView(
    generics.UpdateAPIView
):

    serializer_class = CompanyVerificationSerializer
    permission_classes = [IsAdmin]

    queryset = Company.objects.all()

    http_method_names = ["patch"]

    def perform_update(self, serializer):

        serializer.save()