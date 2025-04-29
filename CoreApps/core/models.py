#CoreApps/core/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class City(models.Model):
    nombre = models.CharField(_("Ciudad"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Ciudad")
        verbose_name_plural = _("Ciudades")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    ciudad = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='zonas'
    )
    nombre = models.CharField(_("Zona"), max_length=100)

    class Meta:
        verbose_name = _("Zona")
        verbose_name_plural = _("Zonas")
        unique_together = ('ciudad', 'nombre')
        ordering = ['ciudad__nombre', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.ciudad.nombre})"