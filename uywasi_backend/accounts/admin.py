"""Accounts app admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Local
from uywasi_backend.accounts.models import User, UserAccount, Following


class UserAccountAdmin(admin.StackedInline):
    """
    UserAccountAdmin.

    This class extends from admin.ModelAdmin, it is used for manage user accounts.
    """
    model = UserAccount
    can_delete = False
    verbose_name_plural = 'User Account'

    fieldsets = (
        (
            "",
            {
                "fields": (
                    ("profile_photo"),
                    ("phone"),
                    ("biography"),
                )
            },
        ),
        ("Ubication", {"fields": (("longitude"), ("latitude"))}),
        ("Verification", {"fields": (("is_verified"), ("is_confirmed"))}),
        ("History", {"fields": ("created", "modified")}),
    )

    readonly_fields = ("created", "modified")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User admin overrided for include UserAccount data."""
    list_filter = ("useraccount__created", "useraccount__modified") + BaseUserAdmin.list_filter
    inlines = (UserAccountAdmin,)


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    """
    FollowingAdmin.

    This class extends of ModelAdmin, and is used for register a Circle model,
    and modified the list_display, list_filter, search_fields and fieldsets.
    """

    list_display = ("id", "user_account_from", "user_account_to", "created")
    list_filter = ("created", "modified")
    search_fields = (
        "user_account_from__username",
        "user_account_to__username",
        "user_account_from__first_name",
        "user_account_to__first_name",
        "user_account_from__last_name",
        "user_account_to__last_name",
    )
    fieldsets = (
        (
            "Following Information",
            {"fields": (("user_account_from", "user_account_to"), ("created", "modified"))},
        ),
    )
    readonly_fields = ("created", "modified")
