# api/views.py
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# 1) ListView — retrieve all books (GET)
class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny, permissions.IsAdminUser]  # public read

# 2) DetailView — retrieve a single book by ID (GET)
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # public read

# 3) CreateView — add a new book (POST)
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only authenticated users can create

    def perform_create(self, serializer):
        # set the owner to the current user (optional)
        serializer.save(owner=self.request.user)

# 4) UpdateView — modify an existing book (PUT/PATCH)
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]# only owner can update

# 5) DeleteView — remove a book (DELETE)
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only owner can delete
