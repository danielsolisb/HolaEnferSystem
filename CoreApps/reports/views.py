from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from CoreApps.appointments.models import AppointmentStatus
from .models import ConsentOrPrescription, Report
from .forms import ConsentOrPrescriptionForm, ReportForm
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import datetime
from io import BytesIO
from django.core.files.base import ContentFile

def generar_consentimiento_pdf(consentimiento_instance):
    """
    Genera un PDF de consentimiento y lo guarda en el campo documento_generado del consentimiento_instance.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    paciente = consentimiento_instance.report.appointment.paciente
    cita = consentimiento_instance.report.appointment

    # Datos principales
    paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    paciente_cedula = paciente.cedula
    fecha_cita = cita.horario.fecha.strftime('%d/%m/%Y') if cita.horario and cita.horario.fecha else "Fecha no registrada"
    hora_cita = cita.hora.strftime('%H:%M') if cita.hora else "Hora no registrada"

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 3*cm, "Documento de Consentimiento Informado")

    # Texto
    texto = (
        f"Yo, {paciente_nombre}, con cédula {paciente_cedula}, "
        f"acepto y doy mi consentimiento para el procedimiento aplicado el día {fecha_cita} "
        f"a las {hora_cita}. Declaro que he sido informado adecuadamente y acepto de forma voluntaria."
    )
    c.setFont("Helvetica", 12)
    c.drawString(3*cm, height - 5*cm, texto)

    # Firma
    if consentimiento_instance.firma_digital:
        firma_path = consentimiento_instance.firma_digital.path
        c.drawImage(firma_path, 3*cm, height - 14*cm, width=8*cm, preserveAspectRatio=True)

    # Pie de página
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(3*cm, 3*cm, f"Fecha de generación del documento: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.showPage()
    c.save()

    buffer.seek(0)
    filename = f"consentimiento_{consentimiento_instance.pk}.pdf"
    consentimiento_instance.documento_generado.save(filename, ContentFile(buffer.read()))
    buffer.close()

class ConsentOrPrescriptionCreateView(LoginRequiredMixin, View):
    template_name = 'main/reports/consent_or_prescription_form.html'

    def get(self, request, *args, **kwargs):
        report_id = request.GET.get('report')
        report = get_object_or_404(Report, pk=report_id)
        instance, created = ConsentOrPrescription.objects.get_or_create(report=report)
        form = ConsentOrPrescriptionForm(instance=instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        report_id = request.GET.get('report')
        report = get_object_or_404(Report, pk=report_id)
        instance, created = ConsentOrPrescription.objects.get_or_create(report=report)
        form = ConsentOrPrescriptionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance.tipo == ConsentOrPrescription.CONSENTIMIENTO:
                generar_consentimiento_pdf(instance)
                instance.save()
            return redirect('reports:report-list')  # Ajusta si deseas otro destino
        return render(request, self.template_name, {'form': form})

# Lista de reportes
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main/reports/report_list.html'
    context_object_name = 'reports'
    ordering = ['-fecha_hora_reporte']

# Detalle de un reporte
class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main/reports/report_detail.html'
    context_object_name = 'report'

# Crear un reporte

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main/reports/report_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['appointment'] = self.request.GET.get('appointment')
        return initial

    def form_valid(self, form):
        form.instance.enfermero = self.request.user
        cita = form.instance.appointment

        estado_confirmado, created = AppointmentStatus.objects.get_or_create(nombre="Confirmada")
        cita.estado = estado_confirmado
        cita.save()

        self.object = form.save()  # ← Guardas manualmente
        return redirect(
            reverse('reports:consent-or-prescription-create') + f'?report={self.object.pk}'
        )

# Editar un reporte
class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main/reports/report_form.html'
    success_url = reverse_lazy('reports:report-list')

# Eliminar un reporte
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main/reports/report_confirm_delete.html'
    success_url = reverse_lazy('reports:report-list')
