from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    - Authenticated users can view books (list, retrieve)
    - Admin users can create, update, delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Filtering / searching / ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']

    def get_permissions(self):
        # Allow any authenticated user to list/retrieve
        # Require admin for any other actions (create/update/delete)
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [perm() for perm in permission_classes]
