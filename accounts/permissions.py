from rest_framework.permissions import BasePermission


class IsCandidate(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "candidate"
        )


class IsRecruiter(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "recruiter"
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == "admin"
                or request.user.is_staff
            )
        )


class IsRecruiterOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == "recruiter"
                or request.user.role == "admin"
                or request.user.is_staff
            )
        )