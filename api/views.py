from rest_framework import viewsets
from .models import Books
from .serializers import BooksSerializer

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
