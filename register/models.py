from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from . import choises as ch


class User(AbstractUser):

    email = models.EmailField(unique=True)

    middle_name = models.CharField(max_length=150, verbose_name='Отчество', blank=True)
    
    place = models.CharField(max_length=255, blank=True)

    educational_institution = models.CharField(max_length=255, blank=True)

    status = models.CharField(max_length=50, choices=ch.STATUS, verbose_name='Статус')

    class_number = models.SmallIntegerField(null=True, verbose_name='Класс/курс')

    phoneNumberRegex = RegexValidator(
        regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    )
    phone = models.CharField(
        validators=[phoneNumberRegex], max_length=16, blank=True, verbose_name='Телефон', default='123'
    )
    
    score = models.IntegerField(default=0, verbose_name='Баланс')

    id_active_event = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
