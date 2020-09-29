"""Circles app Posts views."""

# Django Rest Framework
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins
# Local models
from uywasi_backend.circles.models import Circle
from uywasi_backend.posts.models import Post
# Local serializers
from uywasi_backend.posts.serializers import CirclePostSerializer


class PostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    PostViewSet.

    Allow list the posts of a circle, taking the slugname of url.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        dipatch.

        Take the slugname from url, search the circle with this slugname
        and add it to class attributes.
        """
        circle_slugname = kwargs.get('circle_slugname')
        self.circle = get_object_or_404(
            queryset=Circle,
            slugname=circle_slugname
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        get_queryset.

        If the action is list, then return all posts related to the circle
        obtained on dispatch function.
        """
        if self.action == 'list':
            return Post.objects.filter(
                circle=self.circle
            )

    def get_serializer_class(self):
        """
        get_serializer_class.

        If the action is list, then return CirclePostSerializer as serializer
        class.
        """
        if self.action == 'list':
            return CirclePostSerializer

    def get_permissions(self):
        """
        get_permissions.

        If the action is list, then return a list with an instance of AllowAny
        as permissions.
        """
        if self.action == 'list':
            permissions = (AllowAny,)
        return [permission() for permission in permissions]
