# CoreApps/appointments/models.py

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from CoreApps.customers.models import CustomerProfile
from CoreApps.catalog.models import Service
from django.core.exceptions import ValidationError  # ← Añade esta línea
from CoreApps.catalog.models import Service, Product  # Asegúrate de importar Product también

class AppointmentStatus(models.Model):
    nombre       = models.CharField(_("Estado"), max_length=50, unique=True)
    descripcion  = models.TextField(_("Descripción"), blank=True)

    class Meta:
        verbose_name        = _("Estado de Cita")
        verbose_name_plural = _("Estados de Citas")

    def __str__(self):
        return self.nombre



class Schedule(models.Model):
    enfermero     = models.ForeignKey(
                        settings.AUTH_USER_MODEL,
                        limit_choices_to={'rol': 'enfermero'},
                        on_delete=models.CASCADE,
                        related_name='horarios'
                    )
    fecha         = models.DateField(_("Fecha"))
    hora_inicio   = models.TimeField(_("Hora de inicio"))
    hora_fin      = models.TimeField(_("Hora de fin"))
    disponible    = models.BooleanField(_("Disponible"), default=True)

    class Meta:
        verbose_name        = _("Horario")
        verbose_name_plural = _("Horarios")
        unique_together     = ('enfermero', 'fecha', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"{self.enfermero.nombres} — {self.fecha} {self.hora_inicio}-{self.hora_fin}"



class Appointment(models.Model):
    paciente        = models.ForeignKey(
                         CustomerProfile,
                         on_delete=models.CASCADE,
                         related_name='citas'
                       )
    servicio        = models.ForeignKey(
                         Service,
                         on_delete=models.PROTECT,
                         related_name='citas'
                       )
    enfermero       = models.ForeignKey(
                        settings.AUTH_USER_MODEL,
                        on_delete=models.PROTECT,
                        related_name='citas_asignadas',
                        limit_choices_to={'rol': 'enfermero'},
                        verbose_name=_("Enfermero asignado"),
                        blank=True, null=True
                       )
    horario         = models.ForeignKey(
                         Schedule,
                         on_delete=models.PROTECT,
                         related_name='citas'
                       )
    fecha           = models.DateField(_("Fecha de la cita"), null=True, blank=True)
    hora            = models.TimeField(_("Hora de la cita"), null=True, blank=True)   
    # Ubicación de la cita
    TIPO_UBICACION = [
        ('domicilio', 'En domicilio'),
        ('otro',      'Otra ubicación'),
    ]
    tipo_ubicacion = models.CharField(
        _("Tipo de ubicación"),
        max_length=10,
        choices=TIPO_UBICACION,
        default='domicilio'
    )
    ubicacion = models.TextField(
        _("Ubicación de la cita"),
        blank=True,
        help_text="Si es en domicilio, se copiará la dirección del cliente."
    )
    mapa_ubicacion = models.URLField(
        _("Ubicación en Google Maps"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_("Enlace a Google Maps para la cita.")
    )
    # —————————————————————————————————————————
    estado          = models.ForeignKey(
                         AppointmentStatus,
                         on_delete=models.PROTECT,
                         related_name='citas'
                       )
    asignado_por    = models.ForeignKey(
                         settings.AUTH_USER_MODEL,
                         on_delete=models.SET_NULL,
                         null=True,
                         related_name='citas_agendadas'
                       )
    #productos       = models.ManyToManyField(Product, blank=True, related_name='citas')  # ← NUEVO
    producto        = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Producto aplicado"), null=True, blank=True)  # ← NUEVO (null=True, blank=True)
    doctor_name     = models.CharField(_("Doctor"), max_length=200, blank=True, null=True)
    diagnosis       = models.TextField(_("Diagnóstico"), blank=True, null=True)
    notas           = models.TextField(_("Notas adicionales"), blank=True, null=True)
    fecha_creacion  = models.DateTimeField(_("Creado en"), auto_now_add=True)
    fecha_modifica  = models.DateTimeField(_("Última modificación"), auto_now=True)

    class Meta:
        verbose_name        = _("Cita")
        verbose_name_plural = _("Citas")
        ordering            = ['horario__fecha', 'horario__hora_inicio']

    def __str__(self):
        return f"Cita {self.paciente.nombres} — {self.horario.fecha} {self.hora}"
    
    def clean(self):
        #if self.hora < self.horario.hora_inicio or self.hora > self.horario.hora_fin:
        #    raise ValidationError({
        #        'hora': _(
        #            f"La hora de la cita debe estar entre "
        #            f"{self.horario.hora_inicio} y {self.horario.hora_fin}."
        #        )
        #    })
    
        if self.horario and self.enfermero and self.horario.enfermero != self.enfermero:
            raise ValidationError({
                'horario': _("Este horario no pertenece al enfermero seleccionado.")
            })

        if self.enfermero and self.fecha and self.hora:
            from datetime import timedelta, datetime
        
            hora_inicio_cita = datetime.combine(self.fecha, self.hora)
            hora_fin_cita = hora_inicio_cita + timedelta(hours=1)  # ← asumimos duración de 1 hora
        
            conflictos = Appointment.objects.filter(
                enfermero=self.enfermero,
                fecha=self.fecha
            ).exclude(pk=self.pk)
        
            for cita in conflictos:
                inicio_existente = datetime.combine(cita.fecha, cita.hora)
                fin_existente = inicio_existente + timedelta(hours=1)
        
                # Verifica si se solapan
                if inicio_existente < hora_fin_cita and hora_inicio_cita < fin_existente:
                    raise ValidationError({
                        'hora': _(
                            f"Ya existe una cita para este enfermero entre "
                            f"{inicio_existente.time().strftime('%H:%M')} y {fin_existente.time().strftime('%H:%M')}."
                        )
                    })


        #if self.enfermero and self.fecha and self.hora:
        #    ya_existe = Appointment.objects.filter(
        #        enfermero=self.enfermero,
        #        fecha=self.fecha,
        #        hora=self.hora
        #    )
        #    # Si está editando, excluye el mismo objeto
        #    if self.pk:
        #        ya_existe = ya_existe.exclude(pk=self.pk)
    #
        #    if ya_existe.exists():
        #        raise ValidationError({
        #            'hora': _("Ya existe una cita para este enfermero en esta fecha y hora.")
        #        })
