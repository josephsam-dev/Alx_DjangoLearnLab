# my_api/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):  # Use ListAPIView to match test expectations
    queryset = Book.objects.all()
    serializer_class = BookSerializer
