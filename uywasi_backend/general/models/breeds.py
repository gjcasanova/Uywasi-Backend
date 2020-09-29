"""General app Breeds models."""

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel


class Breed(StandardModel):
    """
    Breed.

    This class represents a breed of animals, all pets have only one breed,
    and each breed belongs to an animal.
    """

    animal = models.CharField(
        help_text=_('This is the animal to which this breed belongs.'),
        max_length=32,
        choices=(('dog', 'Dog'),
                 ('cat', 'Cat'),
                 ('other', 'Other'))
    )

    name = models.CharField(
        help_text=_('This field is the name of the race.'),
        max_length=32,
        null=True,
        blank=True
    )

    description = models.TextField(
        help_text=_('This is a description of the race.'),
        blank=True,
        null=True
    )

    photo = models.ImageField(
        help_text=_('This image will be used as visual help.'),
        upload_to='posts/breeds/photos/',
        blank=True,
        null=True
    )

    def __str__(self):
        """
        __str__.

        Return a string representation formed by name
        of animal and name of breed.
        """
        return '{}/{}'.format(self.get_animal_display(), self.name)

    class Meta(StandardModel.Meta):
        """Meta options. Extended from StandardModel.Meta."""

        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('animal', 'name'),
                name='unique_animal_name'
            ),
        )
