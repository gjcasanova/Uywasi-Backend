"""Circles app urls."""

# Django
from django.urls import path, include
# Django Rest Framework
from rest_framework.routers import DefaultRouter
# Local views
from uywasi_backend.circles.views import CircleViewSet, SubscriptionViewSet, PostViewSet

router = DefaultRouter()

router.register(
    prefix=r'circles',
    viewset=CircleViewSet,
    basename='circles')

router.register(
    prefix=r'circles/(?P<circle_slugname>[^/.]+)/subscriptions',
    viewset=SubscriptionViewSet,
    basename='subscriptions')

router.register(
    prefix=r'circles/(?P<circle_slugname>[^/.]+)/posts',
    viewset=PostViewSet,
    basename='posts')

app_name = 'circles'

urlpatterns = [
    path('', include(router.urls))
]
