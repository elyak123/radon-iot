# Generated by Django 2.2.10 on 2020-05-12 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import radon.users.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instalacion',
            name='consumidor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumidor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='instalacion',
            name='operario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=models.SET(radon.users.utils.get_default_user), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='wisol',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='iot.Wisol'),
        ),
    ]
