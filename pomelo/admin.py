# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from pomelo.models import *

# Register your models here.
""" 
Klasy służące do wyświetlania i edycji odpowiednich modeli na stronie administracyjnej
    By wejść na admina dopiszcie /admin w url
    Login: admin
    Hasło admin123
"""


class ProductDiscountAdmin(admin.ModelAdmin):
    model = ProductDiscount
    list_display = ('product', 'discount')


class ProductReviewsAdmin(admin.ModelAdmin):
    model = Reviews
    list_display = ('user', 'product', 'title', 'text', 'stars', 'date')


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'price', 'description', 'main_image', 'category')


class ProductImagesAdmin(admin.ModelAdmin):
    model = ProductImages
    list_display = ('product', 'image')


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name',)


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('product', 'profile', 'quantity')


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'account_type')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('product', 'storehouse', 'quantity')


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'permission_level')


class StoreHouseAdmin(admin.ModelAdmin):
    model = Storehouse
    list_display = ('city', 'address')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Storehouse, StoreHouseAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)
admin.site.register(Reviews, ProductReviewsAdmin)
