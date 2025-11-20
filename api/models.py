# api/models.py
class Book(models.Model):  # singular "Book"
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
