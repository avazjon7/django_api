from django.contrib import admin
from olcha.models import Category, Group, Product, ProductAttribute, AttributeKey, AttributeValue, Image, Order, Comment

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created_at')
    search_fields = ('id', 'title', 'slug')
    list_filter = ('created_at',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created_at')
    search_fields = ('id', 'title', 'slug')
    list_filter = ('created_at',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created_at')
    search_fields = ('id', 'name', 'slug')
    list_filter = ('created_at',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(AttributeKey)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.register(Image)