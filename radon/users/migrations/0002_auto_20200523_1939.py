# Generated by Django 2.2.10 on 2020-05-24 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gasera',
            options={'verbose_name': 'Gasera', 'verbose_name_plural': 'Gaseras'},
        ),
        migrations.CreateModel(
            name='Precio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('actual', models.BooleanField(default=True)),
                ('gasera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Gasera')),
            ],
            options={
                'verbose_name': 'Precio',
                'verbose_name_plural': 'Precios',
                'unique_together': {('gasera', 'actual')},
            },
        ),
    ]