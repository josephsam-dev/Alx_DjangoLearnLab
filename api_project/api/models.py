from django.db import models
from django.contrib.auth import get_user_model  # ok to import Django libs

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    # owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # example
    def __str__(self):
        return self.title
