from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorList, BookList, BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('books-list/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),  # includes CRUD for books
]
