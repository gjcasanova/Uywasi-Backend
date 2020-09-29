"""Circles app Circles permissions."""

# Django
from django.utils.translation import ugettext as _
# Django Rest Framework
from rest_framework.permissions import BasePermission
# Local models
from uywasi_backend.circles.models import Subscription


class IsCircleActive(BasePermission):
    """
    IsCircleActive.

    This class allows access only if the circle is active.
    """

    message = _('This circle is not active.')

    def has_object_permission(self, request, view, obj):
        """Check the circle is active."""
        return obj.is_active


class IsCircleAdmin(BasePermission):
    """
    IsCircleAdmin.

    This class allows access only if the authenticated user
    is admin of the circle.
    """

    message = _('Only the circle admins can perform this action.')

    def has_permission(self, request, view):
        """
        has_permission.

        This function checks that the authenticated user is admin
        of circle.
        """
        user = request.user
        circle = view.get_object()
        return Subscription.objects.filter(
            user=user, circle=circle, is_admin=True).exists()


class IsCircleMember(BasePermission):
    """
    IsCircleMember.

    This class allows access only if the authenticated user
    is member of the circle.
    """

    message = _('Only the members circle can perform this action.')

    def has_permission(self, request, view):
        """
        has_permission.

        This function checks that the authenticated user is member
        of circle.
        """
        user = request.user
        circle = view.get_object()
        return circle.subscriptions.filter(pk=user.pk).exists()
