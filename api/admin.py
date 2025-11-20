from django.contrib import admin
from .models import Book

# Define the admin class first
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn', 'created_at')
    search_fields = ('title', 'author', 'isbn')

# Register the model using the admin class
admin.site.register(Book, BookAdmin)
