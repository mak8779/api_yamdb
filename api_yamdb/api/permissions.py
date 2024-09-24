from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated and request.user.is_admin
        return request.user.is_authenticated and request.user.is_admin


class IsModeratorOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_moderator:
            return True
        return obj.author == request.user
