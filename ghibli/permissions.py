from rest_framework import permissions


# https://www.django-rest-framework.org/api-guide/permissions/#examples
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.creator is None:
            return True
        return obj.creator == request.user
