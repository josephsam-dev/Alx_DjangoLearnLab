from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer

# Optional ListAPIView (if you want a separate list endpoint)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Full CRUD with custom permissions
class BookViewSet(viewsets.ModelViewSet):
    """
    Custom permissions:
    - Any authenticated user can read (GET, HEAD, OPTIONS)
    - Only admin users can create, update, or delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]  # authenticated users can read
        else:
            permission_classes = [IsAdminUser]      # admin users can write
        return [permission() for permission in permission_classes]
