from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsObjectOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit/manipulate it.
    """

    def has_object_permission(self, request, view, user):
        return request.user.is_superuser or request.user == user
