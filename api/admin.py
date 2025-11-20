from django.contrib import admin
from .models import Books  # <- plural

admin.site.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn', 'created_at')
    search_fields = ('title', 'author', 'isbn')
