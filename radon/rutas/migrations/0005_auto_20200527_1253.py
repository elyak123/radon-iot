# Generated by Django 2.2.10 on 2020-05-27 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutas', '0004_pedido_precio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='ruta',
        ),
        migrations.AddField(
            model_name='pedido',
            name='actualizado',
            field=models.BooleanField(default=False),
        ),
    ]
