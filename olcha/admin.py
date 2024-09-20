from django.contrib import admin

# Register your models here.
from django.contrib import admin

from olcha.models import Product, Category, Group

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Group)
