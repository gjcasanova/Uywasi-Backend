"""Accounts app Followings serializers."""

# Django
from django.utils.translation import ugettext as _

# Django Rest Framework
from rest_framework import serializers

# Local models
from uywasi_backend.accounts.models import Following

# Local serializers
from uywasi_backend.accounts.serializers import UserModelSerializer


class FollowingModelSerializer(serializers.ModelSerializer):
    """
    FollowingModelSerializer.

    This class allows handle the information about an following model.
    """

    def validate(self, data):
        """
        validate.

        This function validates that user_from be different to user_to,
        and that the following does not exists yet.
        """
        validated_data = super().validate(data)
        user_to = validated_data["user_to"]
        user_from = validated_data["user_from"]
        if user_to == user_from:
            raise serializers.ValidationError(
                _("A user cannot follow yourself."))
        if Following.objects.filter(
                user_from=user_from, user_to=user_to).exists():
            raise serializers.ValidationError(
                _("This following already exist."))
        return data

    class Meta:
        """Meta options."""

        model = Following
        fields = ("user_to", "user_from")


class FollowingDetailSerializer(FollowingModelSerializer):
    """
    FollowingDetailSerializer.

    Extends from FollowingModelSerializer, and serializes the user_from
    and user_to fields.
    """

    user_from = UserModelSerializer(read_only=True)
    user_to = UserModelSerializer(read_only=True)

    class Meta(FollowingModelSerializer.Meta):
        """Meta options. Extended FollowingModelSerializer.Meta."""

        fields = FollowingModelSerializer.Meta.fields + ("created",)
