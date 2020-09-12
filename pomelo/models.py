# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from choices import *
from datetime import date
# Create your models here.


class Product(models.Model):
    """ Model Produktu, 2 nazwy pojedyncza i mnoga do wyświetlania potem na stronie """
    name_singular = "Produkt"
    name_plural = "Produkty"
    name = models.CharField(max_length=255, unique=True, null=False, default='def')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    main_image = models.ImageField(upload_to="product_images", null=False, default="nofoto.png")
    category = models.ForeignKey(
        'Category',
        default=0,
        verbose_name='Kategoria',
        related_name='category',
        on_delete=models.CASCADE
    )

    class Meta:
        """ Klasa która automatycznie przydziela w tym przypadku tytuły na stronie """
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

    def __unicode__(self):
        """
        Funkcja ta odpowiada za wyświetlanie nazwy instancji modelu, bez tego bedzie wyświetlać '*model* object'
        """
        return unicode(self.name,) or u''


class ProductDiscount(models.Model):
    """
    Model obniżki ceny, FK produktu oraz sama obniżka w %
    """
    product = models.OneToOneField(
        'Product',
        default=0,
        verbose_name='Produkt',
        related_name='product_discount',
        on_delete=models.CASCADE
    )
    discount = models.IntegerField(default=0)

    def get_discount_price(self):
        """
        Oblicza obniżkę na podstawie 'discount', zamienia ją na procenty
        :return: discount_price w postaci 0.xx
        """
        discount_percent = 100 - self.discount
        if discount_percent < 1:
            discount_percent = 1
        if discount_percent > 100:
            discount_percent = 100
        discount_price = Decimal(
            (self.product.price * discount_percent/100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        )

        return discount_price


class ProductImages(models.Model):
    """
    Model zdjęć produktu, Fk na produkt, odpowiada za te małe zdjęcia w detalach produktu
    """
    product = models.ForeignKey(
        'Product',
        default=None,
        verbose_name='Produkt',
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='product_images', verbose_name='Image', null=True)


class Category(models.Model):
    """
    Model Kategorii, tu chyba nie trzeba za wiele tłumaczyć
    """
    name_singular = "Kategoria"
    name_plural = "Kategorie"
    name = models.CharField(max_length=255, unique=True, null=False, default='def')
    category_image = models.ImageField(
        upload_to='category_images', verbose_name='Image', null=True, default='nofoto.png'
    )

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __unicode__(self):
        return unicode(self.name,) or u''


class Order(models.Model):
    """ Model Zamówień FK Produktu i FK użytkownika oraz ilość zamówionych przedmiotów """
    name_singular = "Zamówienie"
    name_plural = "Zamówienia"
    product = models.ForeignKey(
        'Product',
        related_name='OrderedProduct',
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        'Profile',
        related_name='profile',
        on_delete=models.CASCADE,
        null=True
    )
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"


class Profile(models.Model):
    """ Model użytkownika, FK z typu konta nadającego poziom uprawnień userowi """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name_singular = "Użytkownik"
    name_plural = "Użytkownicy"
    email_confirmed = models.BooleanField(default=False)
    account_type = models.ForeignKey(
        'AccountType',
        verbose_name=u'Użytkownik',
        related_name='AccountType',
        on_delete=models.CASCADE,
        default=1
    )

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"

    def __unicode__(self):
        return unicode(self.user.username,) or u''

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class Status(models.Model):
    """ Model Stanu Magazynowego, FK Produktu, FK Magazynu oraz ilość produktu w danym magazynie """
    name_singular = "Stan"
    product = models.ForeignKey(
        'Product',
        related_name='ProductStatus',
        on_delete=models.CASCADE
    )
    storehouse = models.ForeignKey(
       'Storehouse',
       related_name="StorehouseStatus",
       on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default='0')

    class Meta:
        verbose_name = "Stan"
        verbose_name_plural = "Stan"


class AccountType(models.Model):
    """ Model Typu Konta Użytkownika, np Admin, Moderator """
    name_singular = "Typ Konta"
    name_plural = "Typy Kont"
    name = models.CharField(max_length=255, unique=True, null=False, default='Hej')
    permission_level = models.IntegerField()

    class Meta:
        verbose_name = "Typ Konta"
        verbose_name_plural = "Typy Kont"

    def __unicode__(self):
        return unicode(self.name,) or u''


class Storehouse(models.Model):
    """ Model Magazynu """
    name_singular = "Magazyn"
    name_plural = "Magazyny"
    city = models.CharField(max_length=255, default='', null=True)
    address = models.CharField(max_length=255, default='', null=True)

    class Meta:
        verbose_name = "Magazyn"
        verbose_name_plural = "Magazyny"

    def __unicode__(self):
        return unicode(self.city + " " + self.address) or u''


class Reviews(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_review',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        'Product',
        related_name='product_review',
        on_delete=models.CASCADE,
        null=False,
        default=1
    )
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default="Default Title")
    text = models.TextField()
    stars = models.IntegerField(choices=STAR_CHOICES, null=False, default=1)
