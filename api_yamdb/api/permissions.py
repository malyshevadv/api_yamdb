from rest_framework import permissions


class IsAuthorAdminModerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
        # TODO: add checks for the admin and moderator
