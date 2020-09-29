"""Accounts app Followings views."""

# Django Rest Framework
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework import mixins, viewsets, status
# Local serializers
from uywasi_backend.accounts.serializers import (UserModelSerializer,
                                  FollowingModelSerializer,
                                  FollowingDetailSerializer)
# Local models
from uywasi_backend.accounts.models import User, Following
# Local permissions
from uywasi_backend.accounts.permissions import IsFollowingOwner


class FollowingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    FollowingViewSet.

    This class is a set of functions that allows handles operations over
    the follows of an particular user, such as follows, unfollows,
    retrieves a specific follow, lists follows and others.
    """

    # Filtering and ordering options.

    filter_backends = (OrderingFilter,)
    ordering_fields = ('created',)

    def dispatch(self, request, *args, **kwargs):
        """Retrieve the user from url, and add it to the class attributes."""
        user_username = kwargs.get('user_username')
        self.user = get_object_or_404(
            queryset=User,
            username=user_username,
            is_active=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        get_object.

        Retrieve a Following instance from database where the username of
        user_to is retrieved from url on detail actions, and user_from is
        filtered on get_queryset function.
        """
        user_to_username = self.kwargs.get('pk')
        following = get_object_or_404(
            queryset=self.get_queryset(),
            user_to__username=user_to_username
        )
        self.check_object_permissions(self.request, following)
        return following

    def get_queryset(self):
        """
        get_queryset.

        If the action is list, then returns the users that are followed
        by the user obtained on dispatch function, else returns the following
        instances where user_from is the user obtained on dispatch function.
        """
        if self.action == 'list':
            return self.user.follows.all()
        else:
            return Following.objects.filter(user_from=self.user)

    def get_permissions(self):
        """Define the permissions to use based on action."""
        if self.action in ('list', 'retrieve'):
            permissions = (AllowAny,)
        elif self.action == 'create':
            permissions = (IsAuthenticated,)
        elif self.action == 'destroy':
            permissions = (IsAuthenticated, IsFollowingOwner)
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """Define the serializer class to use based on action."""
        if self.action == 'create':
            return FollowingModelSerializer
        elif self.action == 'list':
            return UserModelSerializer
        elif self.action == 'retrieve':
            return FollowingDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        create.

        Creates a Following instance into database where user_from is
        the authenticated user and the user_to is the user obtained on
        dispatch function.
        """
        data = {
            'user_from': request.user.pk,
            'user_to': self.user.pk
        }
        serializer_class = self.get_serializer_class()
        serialized_data = serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        super().perform_create(serialized_data)
        return Response(status=status.HTTP_201_CREATED)


class FollowersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    FollowersViewSet.

    This class allows obtains the followers of a particular user. This class
    allows filtering and ordering the results too.
    """

    # Filtering and ordering options.

    filter_backends = (OrderingFilter,)
    ordering_fields = ('created',)

    def dispatch(self, request, *args, **kwargs):
        """Retrieve a user from url and add it to class attributes."""
        user_username = kwargs.get('user_username')
        self.user = get_object_or_404(
            queryset=User,
            username=user_username
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        get_queryset.

        Return the users that are following to the user that was
        obtained on dispatch function.
        """
        if self.action == 'list':
            return self.user.user_set.all()

    def get_serializer_class(self):
        """Return UserModelSerializer as serializer class."""
        if self.action == 'list':
            return UserModelSerializer

    def get_permissions(self):
        """Return AllowAny as permissions."""
        if self.action == 'list':
            permissions = (AllowAny,)
        return [permission() for permission in permissions]
