import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clear existing data (optional, for a fresh start)
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create Authors
author1 = Author.objects.create(name="J.K. Rowling", birth_date="1965-07-31")
author2 = Author.objects.create(name="George R.R. Martin", birth_date="1948-09-20")
author3 = Author.objects.create(name="J.R.R. Tolkien", birth_date="1892-01-03")

# Create Books
book1 = Book.objects.create(title="Harry Potter 1", author=author1, published_date="1997-06-26")
book2 = Book.objects.create(title="Harry Potter 2", author=author1, published_date="1998-07-02")
book3 = Book.objects.create(title="A Game of Thrones", author=author2, published_date="1996-08-06")
book4 = Book.objects.create(title="A Clash of Kings", author=author2, published_date="1998-11-16")
book5 = Book.objects.create(title="The Hobbit", author=author3, published_date="1937-09-21")
book6 = Book.objects.create(title="The Lord of the Rings", author=author3, published_date="1954-07-29")

# Create Libraries
library1 = Library.objects.create(name="Central Library")
library2 = Library.objects.create(name="Eastside Library")

# Assign books to libraries
library1.books.add(book1, book3, book5)
library2.books.add(book2, book4, book6)

# Create Librarians
librarian1 = Librarian.objects.create(name="Alice", library=library1)
librarian2 = Librarian.objects.create(name="Bob", library=library2)

print("Sample data populated successfully!")
print("Authors:", Author.objects.count())
print("Books:", Book.objects.count())
print("Libraries:", Library.objects.count())
print("Librarians:", Librarian.objects.count())
