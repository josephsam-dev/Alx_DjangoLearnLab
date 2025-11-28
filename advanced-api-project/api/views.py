from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# ListAPIView for Authors
class AuthorList(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

# ListAPIView for Books
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# ModelViewSet for full CRUD on Books
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
