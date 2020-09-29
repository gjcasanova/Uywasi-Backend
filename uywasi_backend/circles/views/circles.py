"""Circles app Circles views."""

# Django
from django_filters.rest_framework import DjangoFilterBackend
# Django Rest Framework
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets, mixins, status
# Local permissions
from uywasi_backend.circles.permissions import IsCircleAdmin
# Local models
from uywasi_backend.circles.models import Circle
# Local serializers
from uywasi_backend.circles.serializers import (CircleModelSerializer,
                                 CircleDetailSerializer)


class CircleViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    CircleViewSet.

    This class is a set of functions that allow: subscribe, and CRUD
    actions.
    """

    lookup_field = 'slugname'

    # Filtering, ordering and search options

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('slugname', 'name')
    ordering_fields = ('created',)
    filter_fields = ('is_verified',)

    def get_queryset(self):
        """Define the queryset to use, based on the action."""
        if self.action in ('list', 'retrieve', 'update',
                           'partial_update', 'destroy'):
            return Circle.objects.filter(is_active=True)

    def get_permissions(self):
        """Define the permissions to use, based on the action."""
        if self.action == 'create':
            permissions = (IsAuthenticated,)
        elif self.action in ('list', 'retrieve'):
            permissions = (AllowAny,)
        elif self.action in ('update', 'partial_update'):
            permissions = (IsAuthenticated, IsCircleAdmin)
        elif self.action == 'destroy':
            permissions = (IsAuthenticated, IsCircleAdmin)
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """Define the serializer class to use, based on the action."""
        if self.action in ('list', 'create', 'update', 'partial_update'):
            return CircleModelSerializer
        elif self.action == 'retrieve':
            return CircleDetailSerializer

    def create(self, request):
        """Regiter a circle into database."""
        serializer_class = self.get_serializer_class()
        serialized_data = serializer_class(
            data=request.data, context={'request': request})
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(data=serialized_data.data,
                        status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        """Set turn off on attribute is_active of an circle."""
        circle = instance
        circle.is_active = False
        circle.save()
