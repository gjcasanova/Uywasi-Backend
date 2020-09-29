"""Posts app Comments views."""

# Django Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
# Local models
from uywasi_backend.posts.models import Post, Comment


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    CommentViewSet.

    Allow list, destroy and create comments.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch.

        Take the post_id from url, search the Post with this id and add
        it to class attributes.
        """
        post_id = kwargs.get('post_id')
        self.post = get_object_or_404(
            queryset=Post,
            pk=post_id
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        get_queryset.

        Return all comment instances in database.
        """
        return Comment.objects.all()
