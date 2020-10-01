"""Accounts app followings models."""

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel


class Following(StandardModel):
    """
    Following.

    This class represents the following from an user account to other user account.
    A user account can follow to various user accounts.
    """

    user_account_from = models.ForeignKey(
        help_text=_('This is an account that follow.'),
        to='accounts.UserAccount',
        on_delete=models.CASCADE,
        related_name='following_account_from_account'
    )

    user_account_to = models.ForeignKey(
        help_text=_('This is an account that is followed.'),
        to='accounts.UserAccount',
        on_delete=models.CASCADE,
        related_name='following_account_to_account'
    )

    def __str__(self):
        """
        __str__.

        Return a string representation formed by owner user of account_from,
        owner user of account_to and created date.
        """
        return '{} to {} at {}'.format(self.user_account_from.user,
                                       self.user_account_to.user, self.created)

    class Meta(StandardModel.Meta):
        """Meta options. Extended from StandardModel.Meta."""

        constraints = (
            models.UniqueConstraint(
                fields=('user_account_from', 'user_account_to'),
                name='unique_user_account_from_user_account_to'
            ),
        )
