from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS'] or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsModeratorOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_moderator:
            return True
        return obj.author == request.user
