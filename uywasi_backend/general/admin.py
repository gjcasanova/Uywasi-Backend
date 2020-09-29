"""General app admin."""

# Django
from django.contrib import admin
# Local
from uywasi_backend.general.models import Breed


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """
    BreedAdmin.

    This class extends of ModelAdmin, and is used for register a Breed
    model, and modified the list_display, list_filter, search_fields and
    fieldsets.
    """

    list_display = ('name', 'animal', 'description')
    list_filter = ('animal', 'created', 'modified')
    search_fields = ('name',)
    fieldsets = (
        ('Breed Information', {
            'fields': (('name',),
                       ('animal', 'photo'),
                       ('description'),
                       ('created', 'modified'))
        }),
    )
    readonly_fields = ('created', 'modified')
