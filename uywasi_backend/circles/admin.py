"""Circles app admin."""

# Django
from django.contrib import admin
# Local
from uywasi_backend.circles.models import Circle, Subscription


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """
    CircleAdmin.

    This class extends of ModelAdmin, and is used for register a Circle model,
    and modified the list_display, list_filter, search_fields and fieldsets.
    """

    list_display = ('slugname', 'name', 'is_verified')
    list_filter = ('is_verified', 'created', 'modified')
    search_fields = ('slugname', 'name')
    fieldsets = (
        ('Profile Information', {
            'fields': (('name', 'slugname'),
                       ('about'),
                       ('created', 'modified'))
        }),
        ('Identification', {
            'fields': (('is_verified'),)
        })
    )
    readonly_fields = ('created', 'modified')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    SubscriptionAdmin.

    This class extends of ModelAdmin, and is used for register a Subscription
    model, and modified the list_display, list_filter, search_fields and
    fieldsets.
    """

    list_display = ('id', 'user', 'circle', 'created', 'is_admin')
    list_filter = ('is_admin', 'created', 'modified')
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name', 'circle__name', 'circle__slug_name')
    fieldsets = (
        ('Subscription Information', {
            'fields': (('user', 'circle'),
                       ('is_admin'),
                       ('created', 'modified'))
        }),
    )
    readonly_fields = ('created', 'modified')
