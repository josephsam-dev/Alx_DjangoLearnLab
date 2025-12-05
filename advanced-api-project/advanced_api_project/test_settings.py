"""
Test settings for advanced_api_project.
Inherits from base settings but overrides for test isolation:
- Uses in-memory SQLite database (fast, no side effects)
- Disables migrations for speed (if needed)
- Simplified logging
"""

from .settings import *  # noqa: F401, F403

# Test database: in-memory SQLite for speed and isolation
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # In-memory database
    }
}

# Disable migrations during tests if you want faster test runs
# (Django will create tables from models directly)
# Uncomment below if needed:
# class DisableMigrations(dict):
#     def __missing__(self, key):
#         return None
# MIGRATION_MODULES = DisableMigrations()

# Simplify logging for tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',  # Only show errors during tests
    },
}

# Optional: Speed up password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Optional: CSRF trusted origins (leave empty for tests)
CSRF_TRUSTED_ORIGINS = []
