"""Circles app Subscriptions models."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel
from uywasi_backend.accounts.models import User
from uywasi_backend.circles.models import Circle


class Subscription(StandardModel):
    """
    Subscription.

    Represent a subscription from an user to a circle.
    A user can subscribe to one or more circles.
    """

    user = models.ForeignKey(
        help_text=_('This is the user subscribed.'),
        to=User,
        on_delete=models.CASCADE
    )

    circle = models.ForeignKey(
        help_text=_('This is the circle which the user subcribed.'),
        to=Circle,
        on_delete=models.CASCADE
    )

    is_admin = models.BooleanField(
        help_text=_('A user can post on a circle only if this field is True. '
                    'This field is False by default, but the circle creator '
                    'can switch this value to True.'),
        default=False,
        blank=True
    )

    def __str__(self):
        """
        __str__.

        Return an string representation formed by user,
        circle and created date.
        """
        return '{} on {} at '.format(self.user, self.circle, self.created)

    class Meta(StandardModel.Meta):
        """Meta options. Extended from StandardModel.Meta."""

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'circle'),
                name='unique_user_circle'
            ),
        )
