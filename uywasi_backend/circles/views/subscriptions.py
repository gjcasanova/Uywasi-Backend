"""Circles app Subscriptions views."""

# Django
from django_filters.rest_framework import DjangoFilterBackend
# Django Rest Framework
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, mixins, status
# Local permissions
from uywasi_backend.circles.permissions import IsSubscriptionOwner
# Local models
from uywasi_backend.circles.models import Circle, Subscription
# Local serializers
from uywasi_backend.circles.serializers import (CircleSubscriptionModelSerializer,
                                 SubscriptionModelSerializer,
                                 SubscriptionDetailSerializer)


class SubscriptionViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                          mixins.ListModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    SubscriptionViewSet.

    This class allows handle operations over circles subscriptions, such as
    subscribe, unsubscribe, list subscriptions of a circle, and others.
    """

    # Filtering and ordering options

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('created',)
    filter_fields = ('is_admin',)

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch.

        Obtain a circle from url and add it as attribute of the class.
        """
        circle_slugname = kwargs.get('circle_slugname')
        self.circle = get_object_or_404(
            queryset=Circle,
            slugname=circle_slugname,
            is_active=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        get_object.

        Obtain the circle name and username from url arguments and returns the
        subscription instance corresponding.
        """
        username = self.kwargs.get('pk')
        subscription = get_object_or_404(
            queryset=self.get_queryset(),
            user__username=username
        )
        self.check_object_permissions(self.request, subscription)
        return subscription

    def get_queryset(self):
        """
        get_queryset.

        Return the subscriptions related to the circle obtained on dispatch
        function.
        """
        return Subscription.objects.filter(circle=self.circle)

    def get_permissions(self):
        """Define the permissions to use, based on action."""
        if self.action in ('list', 'retrieve'):
            permissions = (AllowAny,)
        elif self.action == 'create':
            permissions = (IsAuthenticated,)
        elif self.action == 'destroy':
            permissions = (IsAuthenticated, IsSubscriptionOwner)
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """Define the serializer class to use, based on action."""
        if self.action == 'create':
            return SubscriptionModelSerializer
        elif self.action == 'list':
            return CircleSubscriptionModelSerializer
        elif self.action == 'retrieve':
            return SubscriptionDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        create.

        Create a subscription related to the authenticated user and the
        circle obtained on dispatch function.
        """
        data = {
            'circle': self.circle.pk,
            'user': request.user.pk
        }
        serializer_class = self.get_serializer_class()
        serialized_data = serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        super().perform_create(serialized_data)
        return Response(status=status.HTTP_201_CREATED)
