"""Posts app Comments models."""

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Local models
from uywasi_backend.general.models import StandardModel
from uywasi_backend.accounts.models import User
from uywasi_backend.posts.models import Post


class Comment(StandardModel):
    """
    Comment.

    Represent a comments of a post. A user can comment posts.
    """

    user = models.ForeignKey(
        help_text=_('This is the user who write the comment. It is required.'),
        to=User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        help_text=_('This is the commented post.'),
        to=Post,
        on_delete=models.CASCADE
    )

    content = models.TextField(
        help_text=_('This is the content of the comment.'),
    )

    def __str__(self):
        """
        __str__.

        Return a string representation formed by user,
        post and created date.
        """
        return '{} on {} at '.format(self.user, self.post, self.created)

    class Meta(StandardModel.Meta):
        """Meta options. Extended from StandardModel.Meta."""

        pass
