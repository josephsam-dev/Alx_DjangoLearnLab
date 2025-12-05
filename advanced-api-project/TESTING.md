# Testing Documentation

This document outlines the testing strategy, test cases, how to run tests, and how to interpret results for the Book API.

---

## Testing Strategy

### Approach

We use **Django's built-in test framework** (based on Python's `unittest`) to ensure the Book API endpoints work correctly, enforce permissions, and handle edge cases gracefully.

### Principles

1. **Isolation**: Each test runs in a fresh, isolated test database that is destroyed after completion—no impact on development or production data.
2. **Comprehensive Coverage**: Tests cover:
   - **CRUD Operations**: Create, Read, Update, Delete for books
   - **Filtering/Searching/Ordering**: Data retrieval with query parameters
   - **Authentication & Authorization**: Token auth, permission enforcement (owner-only edit/delete)
   - **Edge Cases**: Invalid data, missing fields, non-existent resources
3. **Fast Execution**: Using in-memory SQLite (`:memory:`), tests complete in < 1 second.

---

## Test Cases

### Setup (Common to All Tests)

- **Users**: Two test users (`owner` and `other`) with authentication tokens
- **Authors**: Two test authors (`Author A`, `Author B`)
- **Books**: Three test books with different owners and authors

### Test Categories

#### 1. **List & Read Operations** (Anonymous Access Allowed)

| Test | Description | Expected Result |
|------|---|---|
| `test_list_books_anonymous_allowed` | GET `/api/books/` without auth | HTTP 200, returns book list |
| `test_retrieve_book_success` | GET `/api/books/{id}/` for existing book | HTTP 200, returns book data |
| `test_retrieve_nonexistent_book` | GET `/api/books/{id}/` for non-existent book | HTTP 404 |

#### 2. **Filtering, Searching & Ordering** (Anonymous Access Allowed)

| Test | Description | Expected Result |
|------|---|---|
| `test_filter_search_ordering` | Filter by title, search by title/author, order by year | Correct results, ordered correctly |

- **Filter**: `?title=Django` → returns books with exact title match
- **Search**: `?search=Django` → searches in title and author name
- **Ordering**: `?ordering=-publication_year` → returns books in descending year order

#### 3. **Create Operations** (Authentication Required)

| Test | Description | Expected Result |
|------|---|---|
| `test_create_requires_auth` | POST to `/api/books/` without auth | HTTP 401 |
| `test_create_with_token` | POST with valid token and data | HTTP 201, owner set to current user |
| `test_create_book_success` | POST valid book data | HTTP 201, book saved with correct owner and data |
| `test_create_book_invalid_year` | POST with future publication year | HTTP 400, validation fails |
| `test_create_book_missing_required_field` | POST without required field (title) | HTTP 400 |

#### 4. **Update Operations** (Owner-Only)

| Test | Description | Expected Result |
|------|---|---|
| `test_update_book_success` | PATCH by owner | HTTP 200, changes saved |
| `test_update_book_full` | PUT by owner with all fields | HTTP 200, all fields updated |
| `test_update_book_not_owner` | PATCH by non-owner | HTTP 403 Forbidden, no changes |
| `test_update_owner_permission` | PATCH attempt by non-owner | HTTP 403 |

#### 5. **Delete Operations** (Owner-Only)

| Test | Description | Expected Result |
|------|---|---|
| `test_delete_book_success` | DELETE by owner | HTTP 204, book removed from DB |
| `test_delete_book_not_owner` | DELETE by non-owner | HTTP 403 Forbidden, book still exists |
| `test_delete_nonexistent_book` | DELETE non-existent resource | HTTP 404 |
| `test_delete_owner_permission` | DELETE permission check | HTTP 403 for non-owner, HTTP 204 for owner |

---

## Running Tests

### Basic Test Run

Run all tests for the `api` app:
```bash
python manage.py test api
```

### Using Test Settings (Recommended)

Use the optimized test settings with in-memory database:
```bash
python manage.py test api --settings=advanced_api_project.test_settings
```

### Verbose Output

Show detailed test results:
```bash
python manage.py test api --verbosity 2 --settings=advanced_api_project.test_settings
```

Output example:
```
test_create_book_success ... ok
test_update_book_not_owner ... Forbidden: /api/books/1/ ... ok
test_delete_book_success ... ok

Ran 17 tests in 0.344s
OK
```

### Run Specific Test

Single test class:
```bash
python manage.py test api.tests.BookAPITestCase
```

Single test method:
```bash
python manage.py test api.tests.BookAPITestCase.test_create_book_success
```

### Test Coverage Report

Install coverage tool:
```bash
pip install coverage
```

Generate coverage report:
```bash
coverage run --source='api' manage.py test api --settings=advanced_api_project.test_settings
coverage report
```

Example output:
```
Name                          Stmts   Miss  Cover
------------------------------------------------
api/__init__.py                  0      0   100%
api/admin.py                     4      0   100%
api/models.py                   10      0   100%
api/permissions.py               8      0   100%
api/serializers.py              12      0   100%
api/tests.py                   120      5    96%
api/views.py                    35      0   100%
api/urls.py                      2      0   100%
------------------------------------------------
TOTAL                          191      5    97%
```

Generate HTML coverage report:
```bash
coverage html
```
Then open `htmlcov/index.html` in your browser.

---

## Interpreting Test Results

### Success Output

```
Ran 17 tests in 0.344s
OK
```

- ✅ All tests passed
- ✅ No failures or errors
- ✅ No test data persisted (database isolated)

### Failure Output

```
FAILED (failures=1, errors=0)
```

Each failure shows:
- Test name
- Assertion that failed
- Expected vs. actual value
- Line number in test file

Example:
```
AssertionError: 401 != 200
```
→ Expected HTTP 200, but got 401 (unauthorized).

### Error Output

```
ERROR: test_create_book_success (api.tests.BookAPITestCase)
Traceback:
  ...
  File "api/views.py", line 12, in perform_create
    serializer.save(owner=self.request.user)
AttributeError: 'AnonymousUser' object has no attribute 'username'
```

→ Code raised an unexpected exception during test execution.

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `AssertionError: 404 != 200` | Endpoint not found | Check URL routing in `urls.py` |
| `AssertionError: 401 != 201` | Missing authentication | Ensure token is set with `credentials()` |
| `AssertionError: 403 != 204` | Permission denied | Verify `IsOwnerOrReadOnly` logic |
| `IntegrityError` | Duplicate/invalid data | Check model constraints and test data |
| `FieldError: Unsupported lookup` | Invalid filter field | Update `filterset_fields` in views |

---

## Test Database Isolation

### How It Works

1. **Before each test run**: Django creates a fresh test database from migrations
2. **During tests**: All queries use the test database
3. **After each test**: Transactions are rolled back (or the test DB is destroyed)
4. **Result**: Zero impact on development/production databases

### Test DB Options

**Option 1: Default (File-based SQLite)**
```bash
python manage.py test api
```
- Creates a temporary SQLite file
- Slower but closer to production

**Option 2: In-Memory SQLite** (Recommended)
```bash
python manage.py test api --settings=advanced_api_project.test_settings
```
- Fastest (no disk I/O)
- Completely isolated
- Perfect for CI/CD

### Verify Isolation

Check that development database is unchanged after test run:
```bash
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM api_book;"
```
→ Should return your original book count, unchanged by tests.

---

## Test Files

- **`api/tests.py`**: All test cases (17 total)
- **`advanced_api_project/test_settings.py`**: Test-specific Django settings (in-memory DB, fast hashing)
- **`TESTING.md`**: This documentation

---

## Summary

**Current Test Suite:**
- **17 total tests**
- **Categories**: List (3), Filter/Search/Ordering (1), Create (5), Update (4), Delete (4)
- **Execution time**: ~0.3 seconds (in-memory DB)
- **Coverage**: 97% of API code

**Quick Start:**
```bash
# Run all tests
python manage.py test api --settings=advanced_api_project.test_settings --verbosity 2

# Run specific test
python manage.py test api.tests.BookAPITestCase.test_create_book_success

# Check coverage
coverage run --source='api' manage.py test api --settings=advanced_api_project.test_settings
coverage report
```

**Key Guarantees:**
✅ CRUD operations work correctly  
✅ Filtering/searching/ordering functional  
✅ Authentication enforced  
✅ Owner-only operations protected  
✅ Edge cases handled (invalid data, 404s, etc.)  
✅ Zero impact on development/production data

