from rest_framework import serializers
from book.models import Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        context = super(BookSerializer, self).to_representation(instance)
        context['updated_at'] = datetime.now()
        return context
