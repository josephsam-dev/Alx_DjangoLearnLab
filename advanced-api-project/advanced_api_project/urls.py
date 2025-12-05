from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from api.views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    # Redirect root to the API index
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Note: `api.urls` defines explicit book views; the router already
    # registers `books/` via `BookViewSet`. Including both would create
    # duplicate URL patterns for the same paths, so `api.urls` is not
    # included here to avoid conflicts.
]
