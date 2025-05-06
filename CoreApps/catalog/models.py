#CoreApps/catalog/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    #neptuno agregar
    nombre = models.CharField(_("Nombre del servicio"), max_length=100)
    descripcion = models.TextField(_("Descripción del servicio"), blank=True)
    precio = models.DecimalField(_("Precio"), max_digits=8, decimal_places=2)
    activo = models.BooleanField(_("Activo"), default=True)
    # --- NUEVO CAMPO --- g 
    requires_removal = models.BooleanField(
        _("Requiere Cita de Retiro"),
        default=False,
        help_text=_("Marcar si este servicio necesita una cita de seguimiento para retiro (ej. Suero).")
    )
    # --- FIN NUEVO CAMPO ---
    class Meta:
        verbose_name = _("Servicio")
        verbose_name_plural = _("Servicios")

    def __str__(self):
        return self.nombre

class Product(models.Model):
    #neptuno agregar campo
    nombre = models.CharField(_("Nombre del producto"), max_length=100)
    descripcion = models.TextField(_("Descripción del producto"), blank=True)
    precio = models.DecimalField(_("Precio"), max_digits=8, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField(_("Cantidad disponible"), default=0)
    activo = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")

    def __str__(self):
        return self.nombre
