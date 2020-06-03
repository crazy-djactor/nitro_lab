from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from main.models import POS


def CheckPosAuthorization(auth_info):
    """
    Check POS_SN authorization state.
    Token format: `Token pos_sn pos_auth_string`
    """
    if auth_info is None:
        return False
    token_info = auth_info.split(' ')
    if len(token_info) != 3 or token_info[0] != "Token":
        return False

    pos = POS.objects.get(pos_sn=token_info[1], pos_auth_string=token_info[2])
    if pos is None:
        return False
    return True


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


class IsPosAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated pos.
    Authorization information should be `Token pos_sn pos_token`
    """
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_staff):
            return True
        auth_info = request.headers.get("AuthorizationPOS")
        message = 'Your POS must be authorized'
        if CheckPosAuthorization(auth_info=auth_info):
            return True
        raise PermissionDenied(detail=message)


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


class IsAccessible(permissions.BasePermission):
    """
    Only admin user can post,patch and put on SKU
    Only authorized POS can get SKU information
    """
    def has_permission(self, request, view):
        message = "Permission Denied"

        if bool(request.user and request.user.is_staff):
            return True

        if request.method in permissions.SAFE_METHODS:
            auth_info = request.headers.get("Authorization")
            if CheckPosAuthorization(auth_info):
                return True
            raise PermissionDenied(detail=message)
        message = "Permission Denied"
        raise PermissionDenied(detail=message)
