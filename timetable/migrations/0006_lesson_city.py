# Generated by Django 4.1.7 on 2023-04-14 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0005_alter_lesson_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='city',
            field=models.CharField(default='Иркутск', max_length=120, verbose_name='Город'),
        ),
    ]