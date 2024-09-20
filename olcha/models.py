from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

class Group(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Product(models.Model):

    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.SlugField(unique=True)
    quantity = models.PositiveIntegerField(default=1)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='products')
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value, null=True, blank=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

