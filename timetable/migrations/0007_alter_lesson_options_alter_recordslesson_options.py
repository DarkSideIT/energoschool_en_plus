# Generated by Django 4.1.7 on 2023-04-19 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0006_lesson_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'Мероприятие', 'verbose_name_plural': 'Мероприятия'},
        ),
        migrations.AlterModelOptions(
            name='recordslesson',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
    ]
