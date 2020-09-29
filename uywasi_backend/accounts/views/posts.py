"""Accounts app posts views."""

# Django Rest Framework
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework import mixins, viewsets
# Local serializers
from uywasi_backend.posts.serializers import UserPostSerializer
# Local models
from uywasi_backend.accounts.models import User
from uywasi_backend.posts.models import Post


class PostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    PostViewSet.

    Allow list the posts of an user, taking the username from the url.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch.

        Take the username from url, search the user whit this username and
        add it to class attributes.
        """
        user_username = kwargs.get('user_username')
        self.user = get_object_or_404(
            queryset=User,
            username=user_username
        )
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """
        get_serializer_class.

        If the action is list, then return the UserPostSerializer as
        serializer class.
        """
        if self.action == 'list':
            return UserPostSerializer

    def get_queryset(self):
        """
        get_queryset.

        If the action is list, then return all posts of the user obtained
        on dispatch function.
        """
        if self.action == 'list':
            return Post.objects.filter(
                user=self.user
            )

    def get_permissions(self):
        """
        get_permissions.

        If the action is list, then return a list with an instance the AllowAny
        as permissions.
        """
        if self.action == 'list':
            permissions = (AllowAny,)
        return [permission() for permission in permissions]
