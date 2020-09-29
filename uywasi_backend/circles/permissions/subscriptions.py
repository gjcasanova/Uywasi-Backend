"""Circles app Subscriptions permissions."""

# Django
from django.utils.translation import ugettext as _
# Django Rest Framework
from rest_framework.permissions import BasePermission
# Local models
from uywasi_backend.circles.models import Subscription


class IsSubscriptionOwner(BasePermission):
    """
    IsSubscriptionOwner.

    This class allows access only if the authenticated user
    is owner of subscription.
    """

    message = _('Only the owner subscription can perform this action.')

    def has_object_permission(self, request, view, obj):
        """
        has_object_permission.

        This function checks that the authenticated user is owner
        of the subscription.
        """
        return request.user == obj.user
