"""Posts app Posts serializers."""

# Django Rest Framework
from rest_framework import serializers
# Local models
from uywasi_backend.posts.models import Post
from uywasi_backend.circles.models import Circle
from uywasi_backend.accounts.models import User
# Local serializers
from uywasi_backend.accounts.serializers import UserModelSerializer
from uywasi_backend.circles.serializers import CircleModelSerializer
from uywasi_backend.general.serializers import BreedModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    """
    PostModelSerializer.

    Serialize the most important fields of a Post, using SlugRelatedField
    for user and circle with the fields username and slugname respectively.
    """

    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    circle = serializers.SlugRelatedField(
        slug_field='slugname',
        queryset=Circle.objects.all()
    )

    class Meta:
        """Meta options."""

        model = Post
        fields = ('id', 'name', 'information', 'tag',
                  'state', 'color_primary', 'color_secondary', 'size',
                  'photo_first', 'photo_second', 'photo_third', 'latitude',
                  'longitude', 'breed', 'user', 'circle')


class CirclePostSerializer(PostModelSerializer):
    """
    CirclePostSerializer.

    Serialize the most important fields of a Post, but exclude the circle and
    use UserModelSerializer for serialize the user field. It is used for list
    the posts related to a specific circle.
    """

    user = UserModelSerializer(read_only=True)

    class Meta(PostModelSerializer.Meta):
        """Meta options. Extended from PostModelSerializer.Meta."""

        fields = ('id', 'name', 'information', 'tag',
                  'state', 'photo_first', 'user', 'created')


class UserPostSerializer(PostModelSerializer):
    """
    PostUserSerializer.

    Serialize the most important fields of a Post, but exclude the user and
    use StringRelatedField for serialize the circle field. It is used for list
    the posts related to a specific user.
    """

    circle = serializers.StringRelatedField()

    class Meta(PostModelSerializer.Meta):
        """Meta options. Extended from PostModelSerializer.Meta."""

        fields = ('id', 'name', 'information', 'tag',
                  'state', 'photo_first', 'created', 'circle')


class PostDetailSerializer(PostModelSerializer):
    """
    PostDetailSerializer.

    Serialize the same fields of a post that PostModelSerializer, but serialize
    all the related fields using UserModelSerializer, CircleModelSerializer and
    BreedModelSerializer for user, circle and breed fields respectively.
    """

    user = UserModelSerializer(read_only=True)
    circle = CircleModelSerializer(read_only=True)
    breed = BreedModelSerializer(read_only=True)

    class Meta(PostModelSerializer.Meta):
        """Meta options. Extended from PostModelSerializer.Meta."""

        pass
