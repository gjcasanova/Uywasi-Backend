"""Accounts app User permissions."""

# Django
from django.utils.translation import ugettext as _
# Django Rest Framework
from rest_framework import permissions


class IsOwnerAccount(permissions.BasePermission):
    """
    IsOwnerAccount.

    This class allows access only if the requesting user is
    owner of the account.
    """

    message = _('Only account owner can perform this action.')

    def has_object_permission(self, request, view, obj):
        """
        has_object_permission.

        This method checks that the owner of account is
        the same of the requesting user.
        """
        return request.user == obj


class IsNotOwnerAccount(permissions.BasePermission):
    """
    IsNotOwnerAccount.

    This class allows access only if the requesting user is
    not owner of the account.
    """

    message = _('You cannot perform this action in your own account.')

    def has_object_permission(self, request, view, obj):
        """
        has_object_permission.

        This method checks that the owner of account is not
        the same of the requesting user.
        """
        return request.user != obj


class IsConfirmedAccount(permissions.BasePermission):
    """
    IsConfirmedAccount.

    This class allows access only if the requesting user was
    confirmed his email account.
    """

    message = _('The email for this account has not yet been confirmed.')

    def has_object_permission(self, request, view, obj):
        """Return True only if the requesting user account is confirmed."""
        return obj.is_confirmed
