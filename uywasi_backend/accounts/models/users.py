"""Accounts app User models."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel


class User(AbstractUser):
    """
    User.

    This is a custom user model and this is used for Django for
    authentication tasks. First name, Last name, Email and password
    are required, other fields are optionals.
    """

    email = models.EmailField(
        help_text=_('This field is required, unique and '
                    'identification field for login.'),
        unique=True,
        error_messages={
            'unique': _('A user with this email already exists.')
        }
    )

    first_name = models.CharField(
        help_text=_('User\'s first name.'),
        max_length=30,
        blank=False,
        null=False)

    last_name = models.CharField(
        help_text=_('User\'s last name.'),
        max_length=150,
        blank=False,
        null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        """Return username."""
        return self.username

    class Meta:
        """Meta options."""

        ordering = ['username']


class UserAccount(StandardModel):
    """
    UserAccount.

    UserAccount is a class for extends the User class fields. All instance
    of this model is related of an User model instance.
    """

    user = models.OneToOneField(
        help_text=_('User owner of the account. It is mandatory.'),
        to='accounts.User',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    phone = models.CharField(
        help_text=_('Phone number for contact. It is optional.'),
        max_length=16,
        blank=True,
        null=True,
        validators=(
            RegexValidator(
                regex=r'\+?1?\d{9,16}$',
                message=_('Phone number can contains a country code, '
                          'and allow 16 characters maximum. '
                          'Example: +593 0987654321.')
            ),
        )
    )

    biography = models.TextField(
        help_text=_('This field is optional and is an small user '
                    'description.'),
        blank=True,
        null=True
    )

    profile_photo = models.ImageField(
        help_text=_('User profile picture.'),
        upload_to='accounts/profile_pictures/',
        null=True,
        blank=True
    )

    latitude = models.FloatField(
        help_text=_('Latitude of user\'s home location. '
                    'It is a number with decimals.'),
        default=0.0,
        blank=True
    )

    longitude = models.FloatField(
        help_text=_('Longitude of user\'s home location. '
                    'It is a number with decimals.'),
        default=0.0,
        blank=True
    )

    is_active = models.BooleanField(
        help_text=_('An user account is active by default '
                    'but is inactive if the staff suspend this account.'),
        default=True
    )

    is_confirmed = models.BooleanField(
        help_text=_('An account is confirmed only when the '
                    'user verified his email account.'),
        default=False
    )

    is_verified = models.BooleanField(
        help_text=_('An account is verified only when the user\'s '
                    'identity was confirmed by staff.'),
        default=False
    )

    follows = models.ManyToManyField(
        help_text=_('The accounts that this account is following.'),
        to='accounts.UserAccount',
        through='Following',
        through_fields=('user_account_from', 'user_account_to'),
        symmetrical=False
    )

    @property
    def number_of_followers(self):
        """Return the number of followers."""
        return self.useracount_set.all().count()

    @property
    def number_of_follows(self):
        """Return the number of followers."""
        return self.follows.all().count()

    def __str__(self):
        """Return user username"""
        return self.user.username
