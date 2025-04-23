from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from CoreApps.core.models import City

class CustomerProfile(models.Model):
    nombres = models.CharField(_("Nombres"), max_length=100)
    apellidos = models.CharField(_("Apellidos"), max_length=100)
    cedula = models.CharField(_("Cédula"), max_length=20, unique=True)
    telefono = models.CharField(_("Teléfono"), max_length=20)
    email = models.EmailField(_("Correo electrónico"), blank=True, null=True)
    direccion = models.TextField(_("Dirección completa"))
    ciudad = models.ForeignKey(City, on_delete=models.PROTECT, related_name='clientes', blank=True, null=True) # <-- nuevo campo
    fecha_nacimiento = models.DateField(_("Fecha de nacimiento"), blank=True, null=True)
    fecha_registro = models.DateTimeField(_("Fecha de registro"), auto_now_add=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Registrado por"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes_registrados"
    )
    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")

    def __str__(self):
        return f"{self.nombres} ({self.cedula})"


class MedicalHistory(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='medical_histories')
    descripcion = models.TextField(_("Descripción médica"))
    fecha_registro = models.DateTimeField(_("Fecha de registro"), auto_now_add=True)

    class Meta:
        verbose_name = _("Historial Médico")
        verbose_name_plural = _("Historiales Médicos")

    def __str__(self):
        return f"Historial de {self.customer.nombres} - {self.fecha_registro.strftime('%Y-%m-%d')}"
