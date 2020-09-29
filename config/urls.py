# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Accounts app
    path('api/', include('uywasi_backend.accounts.urls', namespace='accounts')),

    # Posts app
    path('api/', include('uywasi_backend.posts.urls', namespace='posts')),

    # Circles app
    path('api/', include('uywasi_backend.circles.urls', namespace='circles')),

    # General app
    path('api/', include('uywasi_backend.general.urls', namespace='general'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
