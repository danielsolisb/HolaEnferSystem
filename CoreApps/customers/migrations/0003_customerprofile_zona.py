# Generated by Django 4.2.4 on 2025-04-28 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_zona'),
        ('customers', '0002_customerprofile_ciudad'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='zona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clientes', to='core.zona', verbose_name='Zona'),
        ),
    ]
