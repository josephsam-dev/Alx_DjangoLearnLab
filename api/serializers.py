from rest_framework import serializers
from .models import Books  # <- plural

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

