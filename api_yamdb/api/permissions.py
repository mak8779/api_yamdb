from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Права доступа для администраторов или только для чтения."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsModeratorOrOwner(BasePermission):
    """Права доступа для модераторов или авторов объекта."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
                obj.author == request.user or
                request.user.is_moderator or
                request.user.is_admin
        )
