#CoreApps/reports/models.py
from django.db import models
from django.conf import settings
from CoreApps.appointments.models import Appointment
from django.utils.translation import gettext_lazy as _

class Report(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE,
        related_name='reporte', verbose_name=_("Cita relacionada")
    )
    enfermero = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, related_name='reportes'
    )
    ubicacion_gps = models.URLField(
        _("Ubicación GPS enfermero"), max_length=500,
        help_text=_("Ubicación del enfermero durante el reporte (link de mapa)")
    )
    notas_novedades = models.TextField(_("Novedades de la cita"))
    valoracion = models.PositiveSmallIntegerField(_("Valoración del servicio"), default=5)
    fecha_hora_reporte = models.DateTimeField(_("Fecha y hora del reporte"), auto_now_add=True)

    class Meta:
        verbose_name = _("Reporte de visita")
        verbose_name_plural = _("Reportes de visitas")

    def __str__(self):
        return f"Reporte - {self.appointment} - {self.fecha_hora_reporte}"

class ConsentOrPrescription(models.Model):
    CONSENTIMIENTO = 'consentimiento'
    RECETA = 'receta'
    TIPO_CHOICES = [
        (CONSENTIMIENTO, 'Consentimiento Informado'),
        (RECETA, 'Receta Médica'),
    ]

    report = models.OneToOneField(
        Report, on_delete=models.CASCADE,
        related_name='consentimiento_o_receta', verbose_name=_("Reporte relacionado")
    )
    tipo = models.CharField(_("Tipo"), max_length=20, choices=TIPO_CHOICES)
    # Para recetas médicas:
    imagen_receta = models.ImageField(
        _("Imagen de la receta"), upload_to='recetas/', blank=True, null=True
    )
    # Para consentimiento informado:
    firma_digital = models.ImageField(
        _("Firma digital"), upload_to='firmas/', blank=True, null=True
    )
    documento_generado = models.FileField(
        _("Documento generado"), upload_to='documentos/', blank=True, null=True
    )
    fecha_hora_creacion = models.DateTimeField(_("Fecha y hora creación"), auto_now_add=True)

    class Meta:
        verbose_name = _("Consentimiento o receta")
        verbose_name_plural = _("Consentimientos y recetas")

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.report}"
