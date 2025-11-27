from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)   # Title of the book
    author = models.CharField(max_length=100)  # Author name

    def __str__(self):
        return f"{self.title} by {self.author}"
