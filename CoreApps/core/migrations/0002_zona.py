# Generated by Django 4.2.4 on 2025-04-28 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Zona')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zonas', to='core.city')),
            ],
            options={
                'verbose_name': 'Zona',
                'verbose_name_plural': 'Zonas',
                'ordering': ['ciudad__nombre', 'nombre'],
                'unique_together': {('ciudad', 'nombre')},
            },
        ),
    ]
