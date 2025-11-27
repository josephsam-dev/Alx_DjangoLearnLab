from django.urls import path
from .views import BookList  # make sure you import your view

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # note the .as_view()
]
