"""General app Breeds serializers."""

# Django Rest Framework
from rest_framework import serializers
# Local models
from uywasi_backend.general.models import Breed


class BreedModelSerializer(serializers.ModelSerializer):
    """
    BreedModelSerializer.

    Serialize the data of a breed, and add the display_animal field.
    """

    display_animal = serializers.SerializerMethodField()

    def get_display_animal(self, obj):
        """Return animal display of breed."""
        return obj.get_animal_display()

    class Meta:
        """Meta options."""

        model = Breed
        fields = ('id', 'name', 'animal', 'display_animal',
                  'photo', 'description')
        read_only_fields = ('id', 'name', 'animal', 'display_animal',
                            'photo', 'description')
