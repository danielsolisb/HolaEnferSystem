from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Appointment
from .forms import AppointmentForm
from .forms import ScheduleForm
from django.http import JsonResponse
from CoreApps.customers.models import CustomerProfile
from CoreApps.core.models import City
from CoreApps.appointments.models import Schedule

# Listar todas las citas (operador y administrador)
class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'main/appointments/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.select_related(
            'paciente', 'servicio', 'horario', 'estado'
        ).prefetch_related('producto').order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Citas"
        context['subtitle'] = "Listado de citas agendadas"
        return context

# Crear nueva cita
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'main/appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:appointment-list')

    def form_valid(self, form):
        form.instance.asignado_por = self.request.user
        form.instance.paciente_id = self.request.POST.get('paciente')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Nueva Cita"
        context['subtitle'] = "Agendar cita para paciente"
        context['ciudades'] = City.objects.all()
        return context

# Detalle de una cita
class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'main/appointments/appointment_detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Detalle de Cita"
        context['subtitle'] = "Información completa"
        return context

# Editar cita
class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'main/appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:appointment-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Cita"
        context['subtitle'] = "Modificar datos"
        context['ciudades'] = City.objects.all()
        return context

# Eliminar cita
class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'main/appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointments:appointment-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar Cita"
        context['subtitle'] = "Confirmación de eliminación"
        return context

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'main/appointments/schedule_form.html'
    success_url = reverse_lazy('appointments:mis-horarios')

    def form_valid(self, form):
        form.instance.enfermero = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Establecer Horarios"
        context['subtitle'] = "Agendar horarios"
        return context

class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'main/appointments/schedule_list.html'
    context_object_name = 'horarios'

    def get_queryset(self):
        return Schedule.objects.filter(enfermero=self.request.user).order_by('-fecha', 'hora_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Horarios"
        context['subtitle'] = "horarios"
        return context

class ScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'main/appointments/schedule_form.html'
    success_url = reverse_lazy('appointments:mis-horarios')

    def test_func(self):
        return self.get_object().enfermero == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Horario"
        context['subtitle'] = "Editar"
        return context

class ScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Schedule
    template_name = 'main/appointments/schedule_confirm_delete.html'
    success_url = reverse_lazy('appointments:mis-horarios')

    def test_func(self):
        return self.get_object().enfermero == self.request.user



def obtener_pacientes_por_ciudad(request):
    ciudad_id = request.GET.get('ciudad_id')
    if not ciudad_id:
        return JsonResponse([], safe=False)

    pacientes = CustomerProfile.objects.filter(ciudad_id=ciudad_id).values('id', 'nombres', 'apellidos', 'cedula')
    data = [
        {
            'id': p['id'],
            'nombre': f"{p['nombres']} {p['apellidos']} ({p['cedula']})"
        }
        for p in pacientes
    ]
    return JsonResponse(data, safe=False)

def obtener_horarios_por_enfermero(request):
    enfermero_id = request.GET.get('enfermero_id')
    if not enfermero_id:
        return JsonResponse([], safe=False)

    horarios = Schedule.objects.filter(enfermero_id=enfermero_id, disponible=True).order_by('fecha', 'hora_inicio')
    data = [
        {
            'id': h.id,
            'texto': f"{h.fecha} - {h.hora_inicio} a {h.hora_fin}"
        }
        for h in horarios
    ]
    return JsonResponse(data, safe=False)