from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    publisher = models.CharField(max_length=100)
    pages = models.IntegerField()

    def __str__(self):
        return f'{self.title} by {self.author}'