# Generated by Django 4.1.7 on 2023-03-20 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_remove_lesson_level_lesson_status_alter_lesson_track'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='theme',
            field=models.TextField(blank=True, verbose_name='Тема'),
        ),
    ]
