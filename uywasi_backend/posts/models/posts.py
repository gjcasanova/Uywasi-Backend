"""Posts app Posts models."""

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel, Breed
from uywasi_backend.accounts.models import User
from uywasi_backend.circles.models import Circle


class Post(StandardModel):
    """
    Post.

    Represent to each pet that has been posted.
    and contains information about the pet's characteristics.
    """

    breed = models.ForeignKey(
        help_text=_('This is the bread of the pet.'),
        to=Breed,
        on_delete=models.PROTECT
    )

    user = models.ForeignKey(
        help_text=_('This is the user owner the post.'),
        to=User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    circle = models.ForeignKey(
        help_text=_(
            'A post can be related to a circle, but it is not required.'),
        to=Circle,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    name = models.CharField(
        help_text=_('This is a name of the pet. It is optional. '
                    'If you do not know the name of pet, '
                    'you can leave this field blank.'),
        max_length=32,
        blank=True,
        null=True
    )

    information = models.TextField(
        help_text=_('This is a description of pet, or other iformation. '
                    'It is required.'),
    )

    tag = models.CharField(
        help_text=_('This field represents the type of post.'),
        max_length=16,
        choices=(('lost', _('Lost')),
                 ('finded', _('Finded')),
                 ('adoption', _('Adoption')))
    )

    state = models.CharField(
        help_text=_('This field indicates if the post is available '
                    'yet or not.'),
        max_length=16,
        blank=True,
        default='open',
        choices=(('open', _('Open')),
                 ('finished', _('Finished')),
                 ('cancelled', _('Cancelled')))
    )

    color_primary = models.CharField(
        help_text=_('This is a principal color of pet. It is required.'),
        max_length=16,
        choices=(('black', _('Black')),
                 ('white', _('White')),
                 ('gray', _('Gray')),
                 ('brown', _('Brown')),
                 ('other', _('Other')))
    )

    color_secondary = models.CharField(
        help_text=_('This is a secondary color of pet. It is optional. '
                    'If the pet does not have more than one color, '
                    'set this field on null.'),
        max_length=16,
        null=True,
        blank=True,
        choices=(('black', _('Black')),
                 ('white', _('White')),
                 ('gray', _('Gray')),
                 ('brown', _('Brown')),
                 ('other', _('Other')))
    )

    size = models.CharField(
        help_text=_('This is the size of pet. The options of small, '
                    'medium, and big.'),
        max_length=1,
        blank=False,
        choices=(('s', _('Small')),
                 ('m', _('Medium')),
                 ('b', _('Big')))
    )

    photo_first = models.ImageField(
        help_text=_('This image helps for identify a pet. '
                    'This field is required. If you do not have '
                    'a photo you can search a photo of similar pet.'),
        upload_to='posts/pets/photos/'
    )

    photo_second = models.ImageField(
        help_text=_('This image helps for identify a pet. '
                    'This field is optional.'),
        upload_to='posts/pets/photos/',
        blank=True,
        null=True
    )

    photo_third = models.ImageField(
        help_text=_('This image helps for identify a pet. '
                    'This field is optional.'),
        upload_to='posts/pets/photos/',
        blank=True,
        null=True
    )

    latitude = models.FloatField(
        help_text=_('This is the latitude of the location. '
                    'This information will be used for contact, '
                    'and for facilitate the search.'),
        default=0.0
    )

    longitude = models.FloatField(
        help_text=_('This is the longitude of the location. '
                    'This information will be used for contact, '
                    'and for facilitate the search.'),
        default=0.0
    )

    def __str__(self):
        """
        __str__.

        Return a string representation formed by
        name of pet, owner user of post and created date.
        """
        return '{} by {} at {}'.format(
            self.name or '-', self.user, self.created)

    class Meta(StandardModel.Meta):
        """Meta options. Extended from StandardModel.Meta."""

        pass
