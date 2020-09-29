"""General app urls."""

# Django
from django.urls import include, path
# Django Rest Framework
from rest_framework.routers import DefaultRouter
# Local views
from uywasi_backend.general.views import BreedViewSet

router = DefaultRouter()

router.register(
    prefix=r'general/breeds',
    viewset=BreedViewSet,
    basename='breeds'
)

app_name = 'general'

urlpatterns = [
    path('', include(router.urls))
]
