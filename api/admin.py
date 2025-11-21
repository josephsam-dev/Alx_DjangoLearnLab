from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published_date', 'isbn', 'created_at')
    list_filter = ('published_date',)
    search_fields = ('title', 'author', 'isbn')
    ordering = ('-created_at',)
