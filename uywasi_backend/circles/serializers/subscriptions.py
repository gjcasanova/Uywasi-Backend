"""Circles app Subscriptions serializers."""

# Django
from django.utils.translation import ugettext as _
# Django Rest Framework
from rest_framework import serializers
# Local models
from uywasi_backend.circles.models import Subscription
# Local serializers
from uywasi_backend.accounts.serializers import UserModelSerializer
from uywasi_backend.circles.serializers import CircleModelSerializer


class SubscriptionModelSerializer(serializers.ModelSerializer):
    """
    SubscriptionModelSerializer.

    Serialize the most important fields of a subscription model.
    """

    def validate(self, data):
        """Validate that the pair circle-user not exist yet."""
        if Subscription.objects.filter(**data).exists():
            raise serializers.ValidationError(
                _('This subscription already exists.'))
        return data

    class Meta:
        """Meta options."""

        model = Subscription
        fields = ('user', 'circle')


class SubscriptionDetailSerializer(SubscriptionModelSerializer):
    """
    SubscriptionDetailSerializer.

    Extend from SubscriptionModelSerializer, and serialize the user and
    circle.
    """

    user = UserModelSerializer(read_only=True)
    circle = CircleModelSerializer(read_only=True)

    class Meta(SubscriptionModelSerializer.Meta):
        """Meta options. Extended from SubscriptionModelSerializer.Meta."""

        fields = SubscriptionModelSerializer.Meta.fields + \
            ('created', 'is_admin')


class CircleSubscriptionModelSerializer(serializers.ModelSerializer):
    """
    CircleSubscriptionModelSerializer.

    Serialize a subscription and serialize the user data.
    """

    user = UserModelSerializer(read_only=True)

    class Meta:
        """Meta options."""

        model = Subscription
        fields = ('user', 'is_admin')
        read_only_fields = ('user', 'is_admin')


class UserSubscriptionModelSerializer(serializers.ModelSerializer):
    """
    CircleSubscriptionModelSerializer.

    Serialize only the circle of a subscription using CircleModelSerializer.
    It is used when list the circles wich the user is subscribed.
    """

    circle = CircleModelSerializer(read_only=True)

    class Meta:
        """Meta options."""

        model = Subscription
        fields = ('circle', 'is_admin')
        read_only_fields = ('circle', 'is_admin')
