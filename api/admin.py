from django.contrib import admin
from .models import Book  # singular, matches class name

admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn', 'created_at')
    search_fields = ('title', 'author', 'isbn')
