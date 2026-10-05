from rest_framework.permissions import BasePermission


class IsJobRecruiter(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["recruiter", "admin"]
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        return obj.job.posted_by == request.user