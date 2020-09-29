"""Accounts app Users serializers."""

# Django
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.translation import ugettext as _
# Django Rest Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
# Local models
from uywasi_backend.accounts.models import User
from uywasi_backend.circles.models import Subscription
from uywasi_backend.posts.models import Post
# Local serializeres
import uywasi_backend.posts
import uywasi_backend.circles
# Local tasks
from uywasi_backend.general.tasks import send_verification_email
# Utils
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """
    UserModelSerializer.

    This class is used for represent the most important information
    of a user.
    """

    class Meta:
        """Meta options."""

        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'profile_photo', 'biography', 'is_verified', 'latitude',
                  'longitude', 'phone', 'number_of_follows',
                  'number_of_followers')
        read_only_fields = ('email', 'is_verified')


class UserProfileModelSerializer(UserModelSerializer):
    """
    UserProfileModelSerializer.

    This class allows extends from UserModelSerializer and adds the fields
    follows and followers, this fields are handled by UserModelSerializer.
    """

    follows = UserModelSerializer(read_only=True, many=True)
    followers = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_followers(self, obj):
        """
        get_followers.

        This function obtains the last three followers of an user.
        It is called for the followers field.
        """
        followers = obj.user_set.all()[:3]
        response = UserModelSerializer(instance=followers, many=True)
        return response.data

    def get_subscriptions(self, obj):
        """
        get_subscriptions.

        This function obtains the last three subscriptions of an user,
        ordered by is_admin attribute.
        """
        subscriptions = Subscription.objects.filter(
            user=obj).order_by('-is_admin')[:3]
        response = circles.serializers.UserSubscriptionModelSerializer(
            instance=subscriptions, many=True)
        return response.data

    def get_posts(self, obj):
        """
        get_posts.

        This function obtains the last thirty posts of an user.
        """
        user_posts = Post.objects.filter(user=obj)[:30]
        response = posts.serializers.PostModelSerializer(
            instance=user_posts, many=True)
        return response.data

    class Meta(UserModelSerializer.Meta):
        """Meta options. Extended from UserModelSerializer.Meta."""

        fields = UserModelSerializer.Meta.fields + \
            ('follows', 'followers', 'subscriptions', 'posts')


class UserLoginSerializer(serializers.ModelSerializer):
    """
    UserLoginSerializer.

    This class is used for login of user. The email field is
    override for skip the Unique validation.
    """

    email = serializers.EmailField(required=True)

    class Meta:
        """Meta options."""

        model = User
        fields = ('email', 'password')

    def validate(self, data):
        """
        validate.

        This method validates that the credentials are correct.
        If the authentication fails, raise a exception with the
        error details.
        """
        validate_data = super().validate(data)
        user = authenticate(
            email=validate_data['email'],
            password=validate_data['password'])
        if not user:
            raise serializers.ValidationError(_('Invalid credentials.'))
        elif not user.is_confirmed:
            raise serializers.ValidationError(
                _('The email for this account has not yet been confirmed.'))
        else:
            self.context['user'] = user
            return validate_data

    def create(self, validated_data):
        """
        create.

        This method get or create an access token related to
        the user that request the access. Returns a
        UserTokenSerializer instance, with the token and the
        user data.
        """
        user = self.context['user']
        token, created = Token.objects.get_or_create(user=user)
        user_token_serialized = {
            'user': UserModelSerializer(instance=user).data,
            'token': token.key
        }
        return UserTokenSerializer(instance=user_token_serialized)


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    UserSignUpSerializer.

    This class is used for creation of new users. This serializer
    contains all required user fields and a password_confirmation.
    Validates that the password be equals to password_confirmation,
    create a user and returns a created User instance.
    """

    password_confirmation = serializers.CharField(
        max_length=128, required=True)

    class Meta:
        """Meta options."""

        model = User
        fields = ('username', 'email', 'password',
                  'password_confirmation', 'first_name', 'last_name')

    def validate(self, data):
        """
        validate.

        Validates that the password be equals to password_confirmation, else,
        raise an exception with the error detail.
        """
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError(
                _('The passwords does not match.'))
        else:
            return data

    def create(self, validate_data):
        """Create a User into database."""
        validate_data.pop('password_confirmation')
        user = User.objects.create_user(**validate_data)
        send_verification_email(user.pk)
        return user


class UserTokenSerializer(serializers.Serializer):
    """
    UserTokenSerializer.

    This class is a wrapper for user and token. Is used for
    return a response after a success login.
    """

    user = UserModelSerializer(read_only=True)
    token = serializers.CharField(read_only=True)


class UserConfirmationSerializer(serializers.Serializer):
    """
    UserConfirmationSerializer.

    This class validates a Json Web token for email confirmation,
    and updates the state of the account to is_confirmed=True.
    """

    token = serializers.CharField(max_length=1024)

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=[
                                 settings.ALGORITHM_TOKEN])
        except jwt.ExpiredSignature:
            raise serializers.ValidationError(_('Link expired.'))
        except jwt.PyJWTError:
            raise serializers.ValidationError(_('Invalid token.'))

        try:
            user = User.objects.get(username=payload['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Invalid token.'))

        if user.is_confirmed:
            raise serializers.ValidationError(
                _('This email account is already confirmed.'))
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError(_('Invalid token.'))
        self.context['user'] = user
        return data

    def save(self):
        """Turn on is_confirmed attribute of an account."""
        user = self.context['user']
        user.is_confirmed = True
        user.save()
