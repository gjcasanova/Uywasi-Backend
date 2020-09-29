"""Accounts app urls."""

# Django Rest Framework
from rest_framework.routers import DefaultRouter
# Django
from django.urls import include, path
# Local views
from uywasi_backend.accounts.views import (
    AccountViewSet, FollowingViewSet, FollowersViewSet, PostViewSet)

router = DefaultRouter()

router.register(
    prefix=r'accounts',
    viewset=AccountViewSet,
    basename='accounts')

router.register(
    prefix=r'accounts/(?P<user_username>[^/.]+)/follows',
    viewset=FollowingViewSet,
    basename='follows'
)

router.register(
    prefix=r'accounts/(?P<user_username>[^/.]+)/followers',
    viewset=FollowersViewSet,
    basename='followers'
)

router.register(
    prefix=r'accounts/(?P<user_username>[^/.]+)/posts',
    viewset=PostViewSet,
    basename='posts'
)


app_name = 'accounts'

urlpatterns = [
    path('', include(router.urls))
]
