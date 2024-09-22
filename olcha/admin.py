from django.contrib import admin
from olcha.models import Product, Category, Group, ProductImage

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category_id', 'image']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'category_id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'discount', 'quantity', 'group_id']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'group_id']



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']
    search_fields = ['product']




