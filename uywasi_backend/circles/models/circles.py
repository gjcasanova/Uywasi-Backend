"""Circles app Circles models."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel
from uywasi_backend.accounts.models import User


class Circle(StandardModel):
    """
    Circle.

    A circle is a profile for a group of users or organizations.
    This groups can be administrated by one or more users.
    """

    name = models.CharField(
        help_text=_('This is the name of circle, '
                    'but not is an identificator.'),
        max_length=64
    )

    slugname = models.SlugField(
        help_text=_('This name is the identificator of circle, '
                    'do not repleace to ID field.'),
        max_length=32,
        unique=True,
        error_messages={
            'unique': _('A circle with this slugname already exists.')
        }
    )

    profile_photo = models.ImageField(
        help_text=_('Photo of circle profile.'),
        upload_to='circles/profile_pictures/',
        blank=True,
        null=True
    )

    cover_photo = models.ImageField(
        help_text=_('Photo of circle cover.'),
        upload_to='circles/cover_pictures/',
        blank=True,
        null=True
    )

    about = models.TextField(
        help_text=_('Description of the circle.'),
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        help_text=_('An circle is verified only when the circle\'s '
                    'identity was confirmed by staff.'),
        default=False
    )

    is_active = models.BooleanField(
        help_text=_('An circle is actived by default, '
                    'but it change when the circle is eliminated.'),
        default=True
    )

    subscriptions = models.ManyToManyField(
        help_text=_('Group of users that are subscripted to this circle.'),
        to=User,
        through='Subscription',
        through_fields=('circle', 'user')
    )

    @property
    def number_of_subscriptions(self):
        """Return the number of subscriptions of circle."""
        return self.subscriptions.all().count()

    def __str__(self):
        """Return slugname."""
        return self.slugname

    class Meta(StandardModel.Meta):
        """Meta options. Extended from StandardModel.Meta."""

        pass
