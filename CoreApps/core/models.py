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
