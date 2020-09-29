"""General app Breeds views."""

# Django
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
# Django Rest Framework
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, mixins
# Local models
from uywasi_backend.general.models import Breed
# Local serializers
from uywasi_backend.general.serializers import BreedModelSerializer


class BreedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    BreedViewSet.

    Allow list and retrieve the breeds registered into database. Includes
    filtering, ordering and search options.
    """

    # Filtering, ordering and search options.

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    ordering_fields = ('name', 'animal')
    filter_fields = ('animal',)

    def get_serializer_class(self):
        """Return BreedModelSerializer as serializer class."""
        if self.action in ('list', 'retrieve'):
            return BreedModelSerializer

    def get_permissions(self):
        """Return AllowAny as permissions."""
        if self.action in ('list', 'retrieve'):
            permissions = (AllowAny,)
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Return all Breed instances as queryset."""
        if self.action in ('list', 'retrieve'):
            return Breed.objects.all()
