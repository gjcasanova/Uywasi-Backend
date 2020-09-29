"""Posts app Posts views."""

# Django Rest Framework
from rest_framework import viewsets
# Local models
from uywasi_backend.posts.models import Post
# Local serializers
from uywasi_backend.posts.serializers import PostModelSerializer, PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    PostViewSet.

    Allow handle CRUD actions over Post model.
    """

    def get_queryset(self):
        """
        get_queryset.

        Return all post instances in database.
        """
        return Post.objects.all()

    def get_serializer_class(self):
        """
        get_serializer_class.

        Define the serializer_class to use based on action.
        """
        if self.action == 'list':
            return PostDetailSerializer
        elif self.action == 'create':
            return PostModelSerializer

    def get_permissions(self):
        """
        get_permissions.

        Define the permissions to use based on action.
        """
        return []
