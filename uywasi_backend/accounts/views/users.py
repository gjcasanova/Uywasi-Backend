"""Accounts app Users views."""

# Django
from django_filters.rest_framework import DjangoFilterBackend
# Django Rest Framework
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins, viewsets, status
# Local serializers
from uywasi_backend.accounts.serializers import (
    UserLoginSerializer, UserModelSerializer, UserSignUpSerializer,
    UserConfirmationSerializer, UserProfileModelSerializer)
# Local models
from uywasi_backend.accounts.models import User
# Local permissions
from uywasi_backend.accounts.permissions import IsOwnerAccount, IsConfirmedAccount


class AccountViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    AccountViewSet.

    This class is a set of functions that allow: Login, confirm,
    and CRUD actions.
    """

    lookup_field = 'username'

    # Filtering, ordering and search options.

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('username', 'first_name', 'last_name')
    ordering_fields = ('username', 'created')
    filter_fields = ('is_verified',)

    def get_queryset(self):
        """Define the queryset to use, based on the action."""
        if self.action in ('login', 'retrieve', 'destroy',
                           'confirm', 'list'):
            return User.objects.filter(is_active=True)
        else:
            return User.objects.all()

    def get_serializer_class(self):
        """Define the serializer class to use, based on the action."""
        if self.action == 'create':
            return UserSignUpSerializer
        elif self.action == 'retrieve':
            return UserProfileModelSerializer
        elif self.action in ('update', 'partial_update', 'list'):
            return UserModelSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'confirm':
            return UserConfirmationSerializer

    def get_permissions(self):
        """Define the permissions needed for perform the action."""
        if self.action in ('list', 'create', 'retrieve', 'login', 'confirm'):
            permissions = (AllowAny,)
        elif self.action == 'destroy':
            permissions = (IsAuthenticated, IsOwnerAccount)
        elif self.action in ('update', 'partial_update'):
            permissions = (IsAuthenticated, IsConfirmedAccount, IsOwnerAccount)
        else:
            permissions = ()
        return [permission() for permission in permissions]

    def create(self, request):
        """Register a user into database."""
        serializer_class = self.get_serializer_class()
        serialized_data = serializer_class(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        user = serialized_data.save()
        serialized_user = UserModelSerializer(instance=user)
        return Response(data=serialized_user.data,
                        status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        """Set turn off on attribute is_active of an user."""
        user = instance
        user.is_active = False
        user.save()

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Authenticate a user."""
        serializer = self.get_serializer_class()
        serialized_data = serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        response = serialized_data.save()
        return Response(data=response.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def confirm(self, request):
        """Confirm an email address."""
        serializer_class = self.get_serializer_class()
        serialized_confirmation = serializer_class(data=request.data)
        serialized_confirmation.is_valid(raise_exception=True)
        serialized_confirmation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
