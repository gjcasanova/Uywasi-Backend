"""Posts app urls."""

# Django
from django.urls import path, include
# Django Rest Framework
from rest_framework.routers import DefaultRouter
# Local views
from uywasi_backend.posts.views import PostViewSet, CommentViewSet

router = DefaultRouter()

router.register(
    prefix=r'posts',
    viewset=PostViewSet,
    basename='posts'
)

router.register(
    prefix=r'posts/(?P<post_id>\d+)/subscriptions',
    viewset=CommentViewSet,
    basename='comments')

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls))
]
