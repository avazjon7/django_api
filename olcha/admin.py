from django.contrib import admin
from olcha.models import Product, Category, Group, ProductImage, Comment, ProductAttribute


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created_at')  # Ensure 'title' exists
    search_fields = ('id', 'title', 'slug')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created_at', 'price', 'discount')  # Ensure 'title' and 'discount' exist
    search_fields = ('id', 'title', 'slug', 'price')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image',  'created_at')  # Ensure 'text' is a valid field
    search_fields = ('id', 'text', 'product__title')  # Use double underscore to search related fields
    list_filter = ('created_at',)




@admin.register(Comment)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'rating', 'product', 'user', 'image']
    search_fields = ['product']


@admin.register(ProductAttribute)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute', 'value', 'created_at')
    search_fields = ('id', 'attribute', 'value')
    list_filter = ('created_at',)
