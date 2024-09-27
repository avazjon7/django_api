from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.utils.text import slugify


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=200, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d/', null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Group(models.Model):
    title = models.CharField(max_length=100)  # Ensure this field exists
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Group, self).save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=100)  # Ensure this field exists
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(BaseModel):
    image = models.ImageField(upload_to='image/%Y/%m/%d/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    is_primary = models.BooleanField(default=False)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='orders')
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    first_payment = models.FloatField(null=True, blank=True, default=0)
    month = models.PositiveSmallIntegerField(default=3, null=True, blank=True,
                                             validators=[MinValueValidator(3), MaxValueValidator(12)])

    @property
    def monthly_payment(self):
        return self.product.price // self.month

    def __str__(self):
        return f'{self.product.name} - {self.user.username} - {self.quantity}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    text = models.CharField(max_length=255)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.title}"

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
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value,null=True)
    image = models.FileField(upload_to='comments', null=True, blank=True)

    def __str__(self):
        return self.product


class AttributeKey(BaseModel):
    key_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.key_name

    class Meta:
        db_table = 'attribute'


class AttributeValue(BaseModel):
    value_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.value_name

    class Meta:
        db_table = 'attribute_value'


class ProductAttribute(BaseModel):
    attribute = models.ForeignKey(AttributeKey, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)