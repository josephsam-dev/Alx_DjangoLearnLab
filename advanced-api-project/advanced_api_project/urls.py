from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import BookViewSet, BookList, BookDetail

# DRF router for BookViewSet
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # include router URLs
    # Optional: separate generic views
    path('api/books-list/', BookList.as_view(), name='book-list'),
    path('api/books-detail/<int:pk>/', BookDetail.as_view(), name='book-detail'),
]
