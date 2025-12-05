from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django_filters import rest_framework as django_filters_rest
from rest_framework import filters

from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly  # your custom object-level permission


# -------------------------
# Generic views (per-endpoint)
# -------------------------

class BookListView(generics.ListAPIView):
    """GET: list books (readable by anyone)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # enable filtering/search/order on this list view
    filter_backends = [django_filters_rest.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year', 'author', 'id']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """GET: retrieve a single book (readable by anyone)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """POST: create a new book (authenticated users only)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # allow unauthenticated to see endpoint, but require login on POST

    def perform_create(self, serializer):
        # attach the current user as owner
        serializer.save(owner=self.request.user)


class BookUpdateView(generics.UpdateAPIView):
    """PUT/PATCH: update a book (only owner may update)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class BookDeleteView(generics.DestroyAPIView):
    """DELETE: delete a book (only owner may delete)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# -------------------------
# ViewSet (alternative)
# -------------------------
class BookViewSet(viewsets.ModelViewSet):
    """
    A full CRUD ViewSet for Book with filtering, searching and ordering.

    Query params examples:
      - Filtering:    ?title=The%20Alchemist
      - Searching:    ?search=alchemist
      - Ordering:     ?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # permissions:
    # - anyone can read
    # - authenticated required for unsafe actions (create)
    # - IsOwnerOrReadOnly enforces object-level checks for update/delete
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Backends to power filtering, search, ordering
    filter_backends = [django_filters_rest.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Simple exact/contains filters
    filterset_fields = ['title', 'author', 'publication_year']

    # Search across these fields with ?search=
    search_fields = ['title', 'author']

    # Fields allowed for ordering and default ordering
    ordering_fields = ['title', 'publication_year', 'author', 'id']
    ordering = ['title']

    def perform_create(self, serializer):
        # ensure owner is set on create
        serializer.save(owner=self.request.user)
