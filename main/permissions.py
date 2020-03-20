from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the device
        is_it = bool(request.user and request.user.is_authenticated)
        return is_it


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        message = 'You must be authenticated'
        is_it = bool(request.user and request.user.is_authenticated)
        if is_it:
            return is_it
        else:
            raise PermissionDenied(detail=message)


class IsAdminOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        message = "Permission Denied"

        if request.method in permissions.SAFE_METHODS:
            is_it = bool(request.user and request.user.is_authenticated)
            if is_it:
                return is_it
            else:
                raise PermissionDenied(detail=message)
        else:
            is_it = bool(request.user and request.user.is_staff)
            if is_it:
                return is_it
            else:
                message = "Permission Denied"
                raise PermissionDenied(detail=message)
