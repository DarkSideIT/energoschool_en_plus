from django.contrib import admin
from .models import *

@admin.register(Product)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'issued')
