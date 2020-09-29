"""Circles app Circles serializers."""

# Django
from django.utils.translation import ugettext as _
# Django Rest Framework
from rest_framework import serializers
# Local models
from uywasi_backend.circles.models import Circle, Subscription
# Local serializers
from uywasi_backend.accounts.serializers import UserModelSerializer


class CircleModelSerializer(serializers.ModelSerializer):
    """
    CircleModelSerializer.

    Serialize the most important fields of a circle.
    """

    def create(self, validate_data):
        """
        create.

        This function saves a circle instance, and register the
        authenticated user as circle admin.
        """
        user = self.context['request'].user
        circle = Circle.objects.create(**validate_data)
        Subscription.objects.create(user=user, circle=circle, is_admin=True)
        return circle

    class Meta:
        """Meta options."""

        model = Circle
        fields = ('name', 'slugname', 'profile_photo', 'cover_photo',
                  'about', 'is_verified', 'number_of_subscriptions')
        read_only_fields = ('is_verified',)


class CircleDetailSerializer(CircleModelSerializer):
    """
    CircleDetailSerializer.

    This class extends from CircleModelSerializer, and serializes
    the subscritions and posts.
    """

    subscriptions = serializers.SerializerMethodField()

    def get_subscriptions(self, obj):
        """Get and serialize the subscriptions of a circle."""
        subscriptions = obj.subscriptions.all()[:3]
        response = UserModelSerializer(
            instance=subscriptions, many=True)
        return response.data

    class Meta(CircleModelSerializer.Meta):
        """Meta options. Extended from Meta Class of CircleModelSerializer."""

        fields = CircleModelSerializer.Meta.fields + ('subscriptions',)
