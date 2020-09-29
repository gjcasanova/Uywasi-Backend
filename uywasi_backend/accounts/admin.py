"""Accounts app admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Local
from uywasi_backend.accounts.models import User, Following


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    UserAdmin.

    This class extends from UserAdmin, change the list_fiter,
    and add the field of custom user, but conserve the fields
    of AbstractUser of Django.
    """

    list_filter = ("created", "modified") + BaseUserAdmin.list_filter
    fieldsets = (
        (
            "Profile Information",
            {
                "fields": (
                    ("profile_photo"),
                    ("phone"),
                    ("biography"),
                    ("created", "modified"),
                )
            },
        ),
        ("Ubication", {"fields": (("longitude"), ("latitude"))}),
        ("Verification", {"fields": (("is_verified"), ("is_confirmed"))}),
        ("Identification", {"fields": ()}),
    ) + BaseUserAdmin.fieldsets

    readonly_fields = ("created", "modified")


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    """
    FollowingAdmin.

    This class extends of ModelAdmin, and is used for register a Circle model,
    and modified the list_display, list_filter, search_fields and fieldsets.
    """

    list_display = ("id", "user_from", "user_to", "created")
    list_filter = ("created", "modified")
    search_fields = (
        "user_from__username",
        "user_to__username",
        "user_from__first_name",
        "user_to__first_name",
        "user_from__last_name",
        "user_to__last_name",
    )
    fieldsets = (
        (
            "Following Information",
            {"fields": (("user_from", "user_to"), ("created", "modified"))},
        ),
    )
    readonly_fields = ("created", "modified")
