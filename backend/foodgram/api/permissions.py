from rest_framework import permissions


class IsAuthorOrSafe(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser):
            return True
        return obj.author.pk == request.user.id

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class UserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser):
            return True
        return obj.id == request.user.id
