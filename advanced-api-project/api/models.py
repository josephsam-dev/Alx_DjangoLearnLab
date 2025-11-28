from django.db import models
from datetime import date

class Author(models.Model):
    """Author model stores the author’s name"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """Book model stores title, publication year, and links to an author"""
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
