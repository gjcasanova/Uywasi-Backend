"""Accounts app Followings permissions."""

# Django
from django.utils.translation import ugettext as _
# Django Rest Framework
from rest_framework import permissions


class IsFollowingOwner(permissions.BasePermission):
    """
    IsFollowingOwner.

    This class allows access only if the requesting user is the owner
    of the following.
    """

    message = _('Only the user that follows can perform this action.')

    def has_object_permission(self, request, view, obj):
        """
        has_object_permission.

        Return True only if the requesting user is the same of
        following.user_from.
        """
        return obj.user_from == request.user
