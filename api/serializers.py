# api/serializers.py
from rest_framework import serializers
from .models import Book  # must match the model name exactly

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
