"""
Unit tests for Book API views.

This module contains comprehensive tests for the Book API endpoints, covering:
- CRUD operations (Create, Read, Update, Delete)
- Filtering, searching, and ordering functionality
- Authentication and permission enforcement
- Edge cases and error handling

All tests use an isolated test database and token authentication.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from api.models import Author, Book


User = get_user_model()


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for the Book API endpoints.
    Tests cover CRUD operations, filtering, searching, ordering, and permission enforcement.
    """

    def setUp(self):
        """Set up test data: users, tokens, authors, and books."""
        # Create test users
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')

        # Create authentication tokens
        self.owner_token = Token.objects.create(user=self.owner)
        self.other_token = Token.objects.create(user=self.other)

        # Create test author
        self.author = Author.objects.create(name='Author A')
        self.author_b = Author.objects.create(name='Author B')

        # Create test books with different owners
        self.book1 = Book.objects.create(
            title='Django Unleashed', publication_year=2019, author=self.author, owner=self.owner
        )
        self.book2 = Book.objects.create(
            title='Learning Python', publication_year=2018, author=self.author, owner=self.other
        )
        self.book3 = Book.objects.create(
            title='Advanced Django', publication_year=2020, author=self.author_b, owner=self.owner
        )

    # ========================
    # LIST & READ TESTS
    # ========================

    def test_list_books_anonymous_allowed(self):
        """Test that anonymous users can list books (GET /api/books/)."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book_success(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django Unleashed')
        self.assertEqual(response.data['publication_year'], 2019)
        self.assertEqual(response.data['author'], self.author.id)

    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist (404)."""
        response = self.client.get('/api/books/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ========================
    # FILTER, SEARCH & ORDERING TESTS
    # ========================

    def test_filter_search_ordering(self):
        """Test filtering by title, searching by title/author, and ordering by year."""
        # Filter by title exact match
        response = self.client.get('/api/books/', {'title': 'Django Unleashed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(b['title'] == 'Django Unleashed' for b in response.data))

        # Search across title and author
        response = self.client.get('/api/books/', {'search': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Django' in b['title'] for b in response.data))

        # Ordering descending by publication_year
        response = self.client.get('/api/books/', {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b['publication_year'] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ========================
    # CREATE TESTS
    # ========================

    def test_create_requires_auth(self):
        """Test that creating a book without authentication returns 401/403."""
        data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author.id}
        response = self.client.post('/api/books/', data)
        # Anonymous should be denied (401 from TokenAuthentication)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_with_token(self):
        """Test successful book creation with valid token."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author.id}
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.owner.id)

    def test_create_book_success(self):
        """Test successful book creation with valid data and verification."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        data = {
            'title': 'Test Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify book was created in the database
        self.assertTrue(Book.objects.filter(title='Test Book').exists())
        book = Book.objects.get(title='Test Book')
        self.assertEqual(book.publication_year, 2021)
        self.assertEqual(book.owner, self.owner)
        self.assertEqual(book.author, self.author)

    def test_create_book_invalid_year(self):
        """Test book creation with future publication year (validation fails)."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        data = {
            'title': 'Future Book',
            'publication_year': 2099,
            'author': self.author.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Book.objects.filter(title='Future Book').exists())

    def test_create_book_missing_required_field(self):
        """Test book creation without required field (title)."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        data = {
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ========================
    # UPDATE TESTS
    # ========================

    def test_update_book_success(self):
        """Test successful partial book update (PATCH) by owner."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        data = {'title': 'Updated Django Title'}
        response = self.client.patch(f'/api/books/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify changes were saved
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Django Title')
        self.assertEqual(self.book1.publication_year, 2019)  # Unchanged

    def test_update_book_full(self):
        """Test full book update (PUT) by owner with all fields."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        data = {
            'title': 'Complete Rewrite',
            'publication_year': 2022,
            'author': self.author_b.id
        }
        response = self.client.put(f'/api/books/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Complete Rewrite')
        self.assertEqual(self.book1.publication_year, 2022)
        self.assertEqual(self.book1.author, self.author_b)

    def test_update_book_not_owner(self):
        """Test that non-owner cannot update the book (403)."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        data = {'title': 'Hacked Title'}
        response = self.client.patch(f'/api/books/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify original title is unchanged
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Django Unleashed')

    def test_update_owner_permission(self):
        """Test owner-only permission for update operations."""
        url = f'/api/books/{self.book1.id}/'
        # other user cannot update owner's book
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        response = self.client.patch(url, {'title': 'Hacked Title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # owner can update
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        response = self.client.patch(url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    # ========================
    # DELETE TESTS
    # ========================

    def test_delete_book_success(self):
        """Test successful book deletion by owner."""
        book_id = self.book1.id
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        response = self.client.delete(f'/api/books/{book_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify book was deleted
        self.assertFalse(Book.objects.filter(id=book_id).exists())

    def test_delete_book_not_owner(self):
        """Test that non-owner cannot delete the book (403)."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        response = self.client.delete(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify book still exists
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist (404)."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        response = self.client.delete('/api/books/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_owner_permission(self):
        """Test owner-only permission for delete operations."""
        url = f'/api/books/{self.book2.id}/'
        # owner of book2 is `other`, so self.owner cannot delete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.owner_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Only the owner can delete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
