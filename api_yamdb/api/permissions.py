from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права для эндпоинтов title, category, genre"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorAdminSuperUserPermissions(permissions.BasePermission):
    """Права для эндпоинтов comment and review"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or any(
            [
                request.user.is_admin,
                request.user.is_moderator,
                obj.author == request.user,
            ]
        )


class IsAdmin(permissions.BasePermission):
    """Права к эндпоиту me/ с запросами patch, get"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
