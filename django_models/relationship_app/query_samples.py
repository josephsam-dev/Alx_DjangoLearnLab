from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
author_name = "J.K. Rowling"
for author in Author.objects.filter(name=author_name).distinct():
    books = Book.objects.filter(author=author)
    print(f"Books by {author.name}: {[book.title for book in books]}")

# 2. List all books in all libraries
for library in Library.objects.all():
    print(f"Books in {library.name}: {[book.title for book in library.books.all()]}")

# 3. Retrieve the librarian for each library
for library in Library.objects.all():
    librarian = Librarian.objects.get(library=library)
    print(f"Librarian of {library.name}: {librarian.name}")
