# relationship_app/query_samples.py
# Usage:
#   python manage.py shell < relationship_app/query_samples.py
# or import functions interactively from the Django shell.

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Return QuerySet of books by a specific author and print them."""
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"Author '{author_name}' does not exist.")
        return []
    books = author.books.all()  # uses related_name 'books'
    print(f"Books by {author.name} ({books.count()}):")
    for b in books:
        print(f" - {b.title}")
    return books

def list_books_in_library(library_name):
    """Return QuerySet of books in a library and print them."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' does not exist.")
        return []
    books = library.books.all()
    print(f"Books in {library.name} ({books.count()}):")
    for b in books:
        print(f" - {b.title} (by {b.author.name})")
    return books

def get_librarian_for_library(library_name):
    """Return the Librarian instance for a library and print name."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' does not exist.")
        return None
    try:
        librarian = library.librarian
        print(f"Librarian for {library.name}: {librarian.name}")
        return librarian
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library.name}.")
        return None

# Optional demo creation when executed via `python manage.py shell < ...`
if __name__ == '__main__':
    if Author.objects.count() == 0 and Book.objects.count() == 0 and Library.objects.count() == 0:
        a1 = Author.objects.create(name='Jane Austen')
        a2 = Author.objects.create(name='Chinua Achebe')

        b1 = Book.objects.create(title='Pride and Prejudice', author=a1)
        b2 = Book.objects.create(title='Emma', author=a1)
        b3 = Book.objects.create(title='Things Fall Apart', author=a2)

        lib = Library.objects.create(name='Central Library')
        lib.books.add(b1, b3)

        Librarian.objects.create(name='Mary', library=lib)

        print('Demo data created.')

    query_books_by_author('Jane Austen')
    list_books_in_library('Central Library')
    get_librarian_for_library('Central Library')
