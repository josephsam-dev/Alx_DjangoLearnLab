# relationship_app/query_samples.py

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
author_name = "J.K. Rowling"
authors = Author.objects.filter(name=author_name).distinct()
for author in authors:
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

# 2. List all books in a library
libraries = Library.objects.all()
for library in libraries:
    print(f"Books in {library.name}: {[book.title for book in library.books.all()]}")

# 3. Retrieve the librarian for each library
for library in libraries:
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian of {library.name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library.name}")

# 4. Example: Add the first book to the first library (if not already added)
if libraries.exists() and Book.objects.exists():
    first_library = libraries.first()
    first_book = Book.objects.first()
    first_library.books.add(first_book)
    first_library.save()
    print(f"Added '{first_book.title}' to {first_library.name}")
