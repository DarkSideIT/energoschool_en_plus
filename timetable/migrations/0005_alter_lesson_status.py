# Generated by Django 4.1.7 on 2023-03-20 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0004_alter_lesson_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('Ученик', 'Ученик'), ('Студент', 'Студент'), ('Родитель', 'Родитель'), ('Общее', 'Общее')], default='Ученик', max_length=120, verbose_name='Статус участника'),
        ),
    ]