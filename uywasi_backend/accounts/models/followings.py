"""Accounts app followings models."""

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel
from uywasi_backend.accounts.models import User


class Following(StandardModel):
    """
    Following.

    This class represents the following from an user to other user.
    A user can follow to various users.
    """

    user_from = models.ForeignKey(
        help_text=_('This is a user that follow.'),
        to=User,
        on_delete=models.CASCADE,
        related_name='following_user_from_user'
    )

    user_to = models.ForeignKey(
        help_text=_('This is a user that is followed.'),
        to=User,
        on_delete=models.CASCADE,
        related_name='following_user_to_user'
    )

    def __str__(self):
        """
        __str__.

        Return an string representation formed by user_from,
        user_to and created date.
        """
        return '{} to {} at '.format(self.user_from,
                                     self.user_to, self.created)

    class Meta(StandardModel.Meta):
        """Meta options. Extended from StandardModel.Meta."""

        constraints = (
            models.UniqueConstraint(
                fields=('user_from', 'user_to'),
                name='unique_user_from_user_to'
            ),
        )
