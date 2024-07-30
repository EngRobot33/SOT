from rest_framework.permissions import BasePermission, SAFE_METHODS


def get_level_permission(required_level):
    class DynamicLevelPermission(BasePermission):
        def has_permission(self, request, view):
            return (
                    request.user.is_authenticated and
                    request.user.permission and
                    request.user.permission.level >= required_level
            )

    return DynamicLevelPermission


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_anonymous
