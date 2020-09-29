"""General app General models."""

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _


class StandardModel(models.Model):
    """
    StandarModel.

    This model does not represent an entity into database but
    is a base standar for all models from uywasi project, although
    maybe the class Meta is modified for the needs of each model.
    """

    created = models.DateTimeField(
        help_text=_('Date time on wich the object was created.'),
        auto_now_add=True
    )

    modified = models.DateTimeField(
        help_text=_('Date time on wich the object was last modified.'),
        auto_now=True
    )

    class Meta:
        """Meta options."""

        abstract = True
        get_latest_by = ['-created', '-modified']
        ordering = ['-created', '-modified']
