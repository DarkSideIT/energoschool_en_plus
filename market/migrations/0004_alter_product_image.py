# Generated by Django 4.1.7 on 2023-04-21 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(max_length=255, upload_to='images\\products', verbose_name='Изображение'),
        ),
    ]
