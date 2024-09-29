from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

from book.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d/', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Group(BaseModel):
    title = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups', null=True)
    image = models.ImageField(upload_to='group/%Y/%m/%d/', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Groups'


class Product(BaseModel):
    title = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField(blank=True)
    discount = models.PositiveIntegerField(default=0, blank=True)
    quantity = models.PositiveIntegerField(default=0, blank=True)
    users_like = models.ManyToManyField(User, related_name='products')

    @property
    def discounted_price(self):
        return self.price * (1 - self.discount / 100) if self.discount else self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Products'


class Image(BaseModel):
    image = models.ImageField(upload_to='products/images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)

    @property
    def is_primary_image(self):
        return self.image if self.is_primary else None

    def __str__(self):
        return f"Image {self.id} for {self.product.title}"


class Order(BaseModel):
    user = models.ForeignKey(get_user_model(),models.CASCADE, null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='orders')
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    first_payment = models.FloatField(null=True, blank=True, default=0)
    month = models.PositiveSmallIntegerField(default=3, null=True, blank=True,
                                             validators=[MinValueValidator(3), MaxValueValidator(12)])


    @property
    def monthly_payment(self):
        return self.product.price // self.month

    def __str__(self):
        return f'{self.product.title} - {self.user.username} - {self.quantity}'


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    message = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='comments/%Y/%m/%d/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value,
                                              null=True)

    def __str__(self):
        return self.message


class AttributeKey(models.Model):
    key_name = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.key_name


class AttributeValue(BaseModel):
    value_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.value_name


class ProductAttribute(models.Model):
    attr_key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE, null=True, blank=True)
    attr_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,related_name='attributes')
