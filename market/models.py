from django.db import models
from register.models import User


class Product(models.Model):
    """Модель товара"""
    title = models.CharField('Название', max_length=255)
    image = models.ImageField('Изображение', max_length=255, upload_to="static/images/products")
    description = models.TextField('Описание', default=None)
    price = models.IntegerField('Цена', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    """Модель заказа"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    issued = models.BooleanField('Выдан', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


    def createOrder(user, product):
        order = Order()
        order.user = user
        order.product = product
        order.save()

        user.score -= product.price
        user.save()