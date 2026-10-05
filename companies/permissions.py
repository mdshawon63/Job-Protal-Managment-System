from rest_framework.permissions import BasePermission


class IsCompanyOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "recruiter",
                "admin",
            ]
        )

    def has_object_permission(self, request, view, obj):

        if request.user.role == "admin":
            return True

        return obj.owner == request.user