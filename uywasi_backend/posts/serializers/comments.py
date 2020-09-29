"""Posts app Comments serializers."""

# Django Rest Framework
from rest_framework import serializers
# Local models
from uywasi_backend.posts.models import Comment


class CommentModelSerializer(serializers.Serializer):
    """
    CommentModelSerializer.

    Serialize the most important fields of a Comment.
    """

    class Meta:
        """Meta options."""

        model = Comment
        fields = '__all__'
