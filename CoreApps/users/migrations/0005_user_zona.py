# Generated by Django 4.2.4 on 2025-04-28 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_zona'),
        ('users', '0004_user_ciudad'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='zona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='enfermeros', to='core.zona', verbose_name='Zona'),
        ),
    ]
