# Generated by Django 5.1.3 on 2024-11-14 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_productocentral_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='puntos',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
