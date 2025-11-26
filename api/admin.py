<<<<<<< HEAD
# api_project/api/admin.py
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author")
=======
from django.contrib import admin

# Register your models here.
>>>>>>> fffbd8bc80147b58f7f8f92c4bec209c333bfdb3
