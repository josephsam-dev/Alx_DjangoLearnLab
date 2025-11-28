from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    # Custom validation: publication year cannot be in the future
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = "__all__"

class AuthorSerializer(serializers.ModelSerializer):
    # Nested books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books"]
