"""General app Accounts tasks."""

# Django
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
# Local
from uywasi_backend.accounts.models import User
# Utils
from datetime import timedelta
import jwt


def send_verification_email(user_pk):
    """
    send_verification_email.

    This task sends an email when a user is created for confirm that
    this user is owner of the email account registered.
    """

    def generate_verificatio_token(user):
        """
        generate_verificatio_token.

        This internal function generates a Json Web Token, this token
        is expirable and contains the username of user.
        """
        expiration_date = timezone.now() + timedelta(
            days=settings.EXPIRATION_TOKEN_DAYS)
        payload = {
            'username': user.username,
            'type': 'email_confirmation',
            'exp': int(expiration_date.timestamp())
        }
        token = jwt.encode(payload, settings.SECRET_KEY,
                           algorithm=settings.ALGORITHM_TOKEN)
        return token.decode()

    user = User.objects.get(pk=user_pk)
    token = generate_verificatio_token(user)
    subject = 'Uywasi | Account verification'
    from_email = 'Uywasi <noreply@uywasi.com>'
    context = {
        'user': user,
        'token': token,
        'url_confirmation': 'https://uywasi.com/login'
    }
    body = render_to_string(
        'emails/accounts/email_verification.html', context=context)
    mail = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[user.email]
    )
    mail.attach_alternative(body, 'text/html')
    mail.send()
