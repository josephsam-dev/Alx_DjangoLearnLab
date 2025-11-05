from django.shortcuts import render
from .models import Book

def index(request):
    books = Book.objects.all().order_by('-publication_year', 'title')
    return render(request, "books/index.html", {"books": books})
