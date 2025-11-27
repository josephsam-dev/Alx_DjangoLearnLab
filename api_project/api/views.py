from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# A generic ListAPIView to list all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()         # Use the Book model as the queryset
    serializer_class = BookSerializer     # Use the BookSerializer
