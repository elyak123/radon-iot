# Generated by Django 2.2.10 on 2021-01-24 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('georadon', '0005_importshapes'),
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='precio',
            name='localidad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='georadon.Localidad'),
        ),
    ]
