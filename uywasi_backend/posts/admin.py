"""Posts app admin."""

# Django
from django.contrib import admin
# Local
from uywasi_backend.posts.models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    CommentAdmin.

    This class extends of ModelAdmin, and is used for register a Comment
    model, and modified the list_display, list_filter, search_fields and
    fieldsets.
    """

    list_display = ('id', 'user', 'post', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('user__username',
                     'user__first_name', 'user__last_name', 'post__name')
    fieldsets = (
        ('Comment Information', {
            'fields': (('user', 'post'),
                       ('content'),
                       ('created', 'modified'))
        }),
    )
    readonly_fields = ('created', 'modified')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    PostAdmin.

    This class extends of ModelAdmin, and is used for register a Post
    model, and modified the list_display, list_filter, search_fields and
    fieldsets.
    """

    list_display = ('name', 'user', 'circle', 'tag', 'state', 'size',
                    'color_primary', 'color_secondary')
    list_filter = ('tag', 'state', 'size', 'breed', 'created', 'modified')
    search_fields = ('name', 'user__username',
                     'user__first_name', 'user_last_name')
    fieldsets = (
        ('Post Information', {
            'fields': (
                ('user', 'circle'),
                ('tag', 'state'),
                ('information'),
                ('created', 'modified')
            )
        }),
        ('Pet Information', {
            'fields': (('name'),
                       ('breed', 'size'),
                       ('color_primary', 'color_secondary'))
        }),
        ('Photos', {
            'fields': (('photo_first'),
                       ('photo_second'),
                       ('photo_third'))
        }),
        ('Ubication', {
            'fields': (('longitude'),
                       ('latitude'))
        })
    )
    readonly_fields = ('created', 'modified')
