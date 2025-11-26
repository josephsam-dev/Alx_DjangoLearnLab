<<<<<<< HEAD
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
=======
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
>>>>>>> fffbd8bc80147b58f7f8f92c4bec209c333bfdb3
    queryset = Book.objects.all()
    serializer_class = BookSerializer
