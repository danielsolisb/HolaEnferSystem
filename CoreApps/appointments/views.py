from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Appointment
from .forms import AppointmentForm
from .forms import ScheduleForm
from django.http import JsonResponse

from CoreApps.core.models import City
from .models import Appointment, Schedule, AppointmentStatus #
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from django.views import View
from django.db.models import Q, Subquery, OuterRef
from django.utils.dateparse import parse_date, parse_datetime
from django.db import transaction # Import transaction


from django.shortcuts import get_object_or_404 # Import get_object_or_404
import json # Import json for request body parsing

#render
from django.shortcuts import render

# --- Modelos y Forms de OTRAS apps (AQUÍ ESTÁ LA CLAVE) ---
from CoreApps.customers.models import CustomerProfile
from CoreApps.customers.forms import CustomerProfileForm # La usas en la API de paciente
from CoreApps.core.models import City, Zona
from CoreApps.catalog.models import Service # Ya importas Service
from CoreApps.catalog.models import Product


User = get_user_model()

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
    template_name = 'main/appointments/appointment_form1.html'
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
    template_name = 'main/appointments/appointment_form1.html'
    success_url = reverse_lazy('appointments:appointment-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Cita"
        context['subtitle'] = "Modificar datos"
        context['ciudades'] = City.objects.all()
        # Datos iniciales solo si existe objeto (modo edición)
        context['ciudad_inicial'] = self.object.paciente.ciudad_id if self.object.paciente else None
        context['paciente_inicial'] = self.object.paciente_id
        context['enfermero_inicial'] = self.object.enfermero_id
        context['horario_inicial'] = self.object.horario_id
        context['hora_inicial'] = self.object.hora.strftime("%H:%M") if self.object.hora else ''
        context['zona_inicial'] = (
            self.object.paciente.zona_id
            if self.object.paciente and self.object.paciente.zona_id
            else None
        )
        context['mapa_inicial'] = self.object.mapa_ubicacion if self.object.mapa_ubicacion else ''

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
        # Base: sólo los horarios del usuario
        qs = Schedule.objects.filter(enfermero=self.request.user)
        # Leemos ?date=YYYY-MM-DD
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                selected = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                selected = timezone.localdate()
        else:
            selected = timezone.localdate()
        # Guardamos en la instancia para usar en el contexto
        self.selected_date = selected
        # Filtramos por esa fecha y ordenamos por hora
        return qs.filter(fecha=selected).order_by('hora_inicio')
    #def get_queryset(self):
    #    return Schedule.objects.filter(enfermero=self.request.user).order_by('-fecha', 'hora_inicio')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': "Lista de Horarios",
            'subtitle': f"Horarios para {self.selected_date.strftime('%d/%m/%Y')}",
            'selected_date': self.selected_date.isoformat(),
        })
        return ctx
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['title'] = "Lista de Horarios"
    #    context['subtitle'] = "horarios"
    #    return context

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
    zona_id   = request.GET.get('zona_id')
    if not ciudad_id:
        return JsonResponse([], safe=False)

    # Base QS filtrada por ciudad, y si llega zona_id, filtramos por zona
    qs = CustomerProfile.objects.filter(ciudad_id=ciudad_id)
    #qs = CustomerProfile.objects.filter(ciudad_id=ciudad_id)
    if zona_id:
        qs = qs.filter(zona_id=zona_id)
    #pacientes = qs.values('id', 'nombres', 'apellidos', 'cedula')
    pacientes = qs.values('id', 'nombres', 'apellidos', 'cedula', 'direccion', 'ubicacion_mapa')
    data = [
        {
            'id': p['id'],
            #'nombre': f"{p['nombres']} {p['apellidos']} ({p['cedula']})"
            'nombre': f"{p['nombres']} {p['apellidos']} ({p['cedula']})",
            'direccion': p['direccion'],
            'mapa': p['ubicacion_mapa']  # Añade esta línea
        }
        for p in pacientes
    ]
    return JsonResponse(data, safe=False)

def obtener_horarios_por_enfermero(request):
    enfermero_id = request.GET.get('enfermero_id')
    if not enfermero_id:
        return JsonResponse([], safe=False)

    horarios = Schedule.objects.filter(enfermero_id=enfermero_id, disponible=True).order_by('fecha', 'hora_inicio')
    data = []

    for h in horarios:
        # Obtener horas ocupadas en citas para este horario
        citas = Appointment.objects.filter(enfermero_id=enfermero_id, horario_id=h.id)
        horas_ocupadas = [c.hora.strftime("%H:%M") for c in citas]

        data.append({
            'id': h.id,
            'texto': f"{h.fecha} - {h.hora_inicio} a {h.hora_fin}",
            'fecha': h.fecha.strftime("%Y-%m-%d"),
            'hora_inicio': h.hora_inicio.strftime("%H:%M"),
            'hora_fin': h.hora_fin.strftime("%H:%M"),
            'ocupadas': horas_ocupadas  # NUEVO CAMPO
        })

    return JsonResponse(data, safe=False)
#def obtener_horarios_por_enfermero(request):
#    enfermero_id = request.GET.get('enfermero_id')
#    if not enfermero_id:
#        return JsonResponse([], safe=False)
#
#    horarios = Schedule.objects.filter(enfermero_id=enfermero_id, disponible=True).order_by('fecha', 'hora_inicio')
#    data = [
#        {
#            'id': h.id,
#            'texto': f"{h.fecha} - {h.hora_inicio} a {h.hora_fin}",
#            'fecha': h.fecha.strftime("%Y-%m-%d"),  # lo importante
#            'hora_inicio': h.hora_inicio.strftime("%H:%M"),
#            'hora_fin': h.hora_fin.strftime("%H:%M"),
#        }
#        for h in horarios
#    ]
#    return JsonResponse(data, safe=False)

def obtener_enfermeros_por_ciudad(request):
    ciudad_id = request.GET.get('ciudad_id')
    zona_id   = request.GET.get('zona_id')
    if not ciudad_id:
        return JsonResponse([], safe=False)

    # Filtramos por ciudad y, si existe zona_id, por esa zona (M2M)
    qs = User.objects.filter(rol='enfermero', ciudad_id=ciudad_id)
    if zona_id:
        qs = qs.filter(zonas__id=zona_id)
    enfermeros = qs.values('id', 'nombres', 'email')
    data = [
        {
            'id': e['id'],
            'nombre': f"{e['nombres']} ({e['email']})"
        }
        for e in enfermeros
    ]
    return JsonResponse(data, safe=False)


#citas de enfermeros logeados para realizar la visualizacion y gestion de las mismas
class AssignedAppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'main/appointments/enfermero_appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        qs = Appointment.objects.filter(enfermero=self.request.user)
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                selected = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                selected = timezone.localdate()
        else:
            selected = timezone.localdate()
        self.selected_date = selected
        return qs.filter(horario__fecha=selected).order_by('horario__fecha', 'hora')
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['selected_date'] = self.selected_date.isoformat()
        ctx['title']    = "Mis Citas Asignadas"
        ctx['subtitle'] = f"Citas para {self.selected_date.strftime('%d/%m/%Y')}"
        return ctx
    
    #def get_queryset(self):
    #    return Appointment.objects.filter(
    #        enfermero=self.request.user
    #    ).order_by('horario__fecha', 'hora')

class AssignedAppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'main/appointments/enfermero_appointment_detail.html'
    context_object_name = 'appointment'


# --- NUEVAS VISTAS API para Call Center ---

class CallCenterAvailabilityAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        zona_id = request.GET.get('zona_id')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if not zona_id or not start_date_str or not end_date_str:
            return JsonResponse({'error': 'Parámetros zona_id, start_date, end_date requeridos'}, status=400)

        try:
            # Validación de Cobertura (Paso 1 del flujo)
            zona = Zona.objects.get(pk=zona_id)
        except Zona.DoesNotExist:
             return JsonResponse({'error': f'Zona con id {zona_id} no encontrada. No hay cobertura.'}, status=404)

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date or start_date > end_date:
            return JsonResponse({'error': 'Fechas inválidas'}, status=400)

        availability_data = {}

        # 1. Encontrar enfermeros para la zona
        # Asume que User tiene ManyToManyField 'zonas'
        nurses_in_zone = User.objects.filter(rol='enfermero', zonas__id=zona_id, is_active=True)
        nurse_ids = list(nurses_in_zone.values_list('id', flat=True))

        if not nurse_ids:
             # Si no hay enfermeros, no hay disponibilidad
             return JsonResponse(availability_data, safe=False)

        # 2. Obtener todos los horarios relevantes
        schedules = Schedule.objects.filter(
            enfermero_id__in=nurse_ids,
            fecha__range=[start_date, end_date],
            disponible=True
        ).values('id', 'enfermero_id', 'fecha', 'hora_inicio', 'hora_fin')

        # 3. Obtener todas las citas existentes relevantes
        existing_appointments = Appointment.objects.filter(
            enfermero_id__in=nurse_ids,
            fecha__range=[start_date, end_date] # Usar el campo fecha de Appointment
        ).values('enfermero_id', 'fecha', 'hora') # Usar fecha y hora de Appointment

        # 4. Procesar y calcular slots libres (Lógica compleja)
        # Esta parte requiere iterar por días, luego por schedules de ese día,
        # generar slots (ej. cada hora), y verificar contra existing_appointments.
        # Es un ejemplo simplificado. Necesitarás ajustar la granularidad (ej. cada 30 min).

        booked_slots = {} # {(enfermero_id, fecha, hora_str): True}
        for appt in existing_appointments:
            if appt['hora']:
                 hora_str = appt['hora'].strftime('%H:%M')
                 key = (appt['enfermero_id'], appt['fecha'], hora_str)
                 booked_slots[key] = True

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            availability_data[date_str] = {}
            # Filtrar schedules para el día actual
            day_schedules = [s for s in schedules if s['fecha'] == current_date]

            # Asumimos slots de 1 hora por simplicidad
            for hour in range(0, 24): # Iterar horas del día
                slot_time = datetime.strptime(f"{hour:02d}:00", '%H:%M').time()
                slot_datetime_start = datetime.combine(current_date, slot_time)

                available_nurses_for_slot = []

                for nurse_id in nurse_ids:
                    is_available = False
                    # Verificar si el enfermero tiene un schedule que cubra este slot
                    for schedule in day_schedules:
                        if schedule['enfermero_id'] == nurse_id and \
                           schedule['hora_inicio'] <= slot_time < schedule['hora_fin']:
                            # Verificar si el slot NO está en las citas existentes
                            slot_key = (nurse_id, current_date, slot_time.strftime('%H:%M'))
                            if slot_key not in booked_slots:
                                is_available = True
                                break # Enfermero disponible en este slot
                    if is_available:
                        available_nurses_for_slot.append(nurse_id)

                if available_nurses_for_slot:
                    availability_data[date_str][slot_time.strftime('%H:%M')] = available_nurses_for_slot

            current_date += timedelta(days=1)


        # Devolver JSON para el calendario
        # Formato: {'YYYY-MM-DD': {'HH:MM': [nurse_id1, nurse_id2], ...}, ...}
        return JsonResponse(availability_data, safe=False)

class CallCenterNursesForSlotAPIView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
        zona_id = request.GET.get('zona_id')
        date_str = request.GET.get('date')
        time_str = request.GET.get('time') # Espera HH:MM

        if not zona_id or not date_str or not time_str:
            return JsonResponse({'error': 'Parámetros zona_id, date, time requeridos'}, status=400)

        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            target_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
             return JsonResponse({'error': 'Formato de fecha (YYYY-MM-DD) o hora (HH:MM) inválido'}, status=400)

        # 1. Encontrar enfermeros para la zona
        nurses_in_zone = User.objects.filter(rol='enfermero', zonas__id=zona_id, is_active=True)

        available_nurses_details = []
        for nurse in nurses_in_zone:
            # 2. Verificar Schedule
            has_schedule = Schedule.objects.filter(
                enfermero=nurse,
                fecha=target_date,
                hora_inicio__lte=target_time,
                hora_fin__gt=target_time, # gt porque la cita empieza a esa hora
                disponible=True
            ).exists()

            if has_schedule:
                # 3. Verificar Citas Existentes
                has_conflict = Appointment.objects.filter(
                    enfermero=nurse,
                    fecha=target_date,
                    hora=target_time # Conflicto exacto a esa hora
                    # Podrías necesitar lógica más compleja si las citas duran > 1 slot
                ).exists()

                if not has_conflict:
                    available_nurses_details.append({
                        'id': nurse.id,
                        'nombre': nurse.nombres
                    })

        return JsonResponse(available_nurses_details, safe=False)

# En appointments/views.py
class CallCenterFindCreatePatientAPIView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            cedula = data.get('cedula')

            if not cedula:
                return JsonResponse({'error': 'Cédula requerida para buscar o crear paciente.'}, status=400)

            customer = CustomerProfile.objects.filter(cedula=cedula).first()

            if customer:
                return JsonResponse({
                    'status': 'found',
                    'patient_id': customer.id,
                    'nombre': customer.nombres,
                    'apellido': customer.apellidos,
                    'telefono': customer.telefono,
                    'email': customer.email,
                    'direccion': customer.direccion, # Devolver más datos si es útil para el form
                    'ciudad_id': customer.ciudad_id,
                    'zona_id': customer.zona_id,
                    'mapa': customer.ubicacion_mapa,
                })
            else:
                # Paciente no encontrado.
                # Ahora, verificamos si se enviaron datos para crear o solo para buscar.
                # Si 'nombres' (u otro campo obligatorio aparte de cedula) está presente, intentamos crear.
                if data.get('nombres') and data.get('apellidos') and data.get('telefono'): # Ajusta según tus campos requeridos
                    form = CustomerProfileForm(data)
                    if form.is_valid():
                        new_customer = form.save(commit=False)
                        new_customer.registrado_por = request.user # Asignar el operador actual
                        new_customer.save()
                        return JsonResponse({
                            'status': 'created',
                            'patient_id': new_customer.id,
                            'nombre': new_customer.nombres,
                            'apellido': new_customer.apellidos,
                            'telefono': new_customer.telefono,
                            'email': new_customer.email,
                            'cedula': new_customer.cedula,
                        }, status=201)
                    else:
                        # Faltan datos o son inválidos para la creación
                        return JsonResponse({
                            'status': 'validation_error_on_create',
                            'message': 'Datos incompletos o inválidos para crear el nuevo paciente.',
                            'errors': form.errors
                        }, status=400)
                else:
                    # Solo se envió cédula y no se encontró el paciente.
                    # Informar al frontend que debe solicitar más datos para la creación.
                    return JsonResponse({
                        'status': 'not_found_enter_details',
                        'message': 'Paciente no encontrado. Por favor, ingrese los detalles para crearlo.'
                        # No es un error 400 aquí, es un estado esperado.
                    })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en la solicitud.'}, status=400)
        except Exception as e:
            # Loggear el error 'e'
            print(f"Error en CallCenterFindCreatePatientAPIView: {e}")
            return JsonResponse({'error': 'Ocurrió un error interno en el servidor.'}, status=500)


class CallCenterAppointmentCreateView(LoginRequiredMixin, View):
    template_name = 'main/appointments/callcenter_create_form.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': "Agendar Cita (Call Center)",
            'subtitle': "Nuevo Agendamiento",
            'ciudades': City.objects.all(),
            'servicios': Service.objects.filter(activo=True),
            'appointment_statuses': AppointmentStatus.objects.all(), # <-- PASAR ESTADOS
            # --- >>> AÑADIR ESTA LÍNEA PARA PASAR PRODUCTOS <<< ---
            'products': Product.objects.filter(activo=True).order_by('nombre'), # Pasa todos los productos activos
            # --- >>> FIN DE LÍNEA A AÑADIR <<< ---
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            # Extraer datos necesarios:
            patient_id = data.get('patient_id')
            service_id = data.get('service_id')
            nurse_id = data.get('nurse_id')
            app_date_str = data.get('application_date')
            app_time_str = data.get('application_time')
            status_id = data.get('status_id') # <-- RECIBIR STATUS_ID
            tipo_ubicacion = data.get('tipo_ubicacion', 'domicilio')
            ubicacion_manual = data.get('ubicacion_manual', '')
            mapa_manual = data.get('mapa_manual', '')
            producto_id = data.get('producto_id') # Se maneja más abajo
            notas_cita = data.get('notas', '')
            doctor_name_cita = data.get('doctor_name', '')

            requires_removal = data.get('requires_removal', False)
            rem_date_str = data.get('removal_date')
            rem_time_str = data.get('removal_time')

            # --- Validación Rigurosa de Datos Esenciales ---
            if not all([patient_id, service_id, nurse_id, app_date_str, app_time_str, status_id]):
                 raise ValueError("Faltan datos esenciales: Paciente, Servicio, Enfermero, Fecha, Hora o Estado de la cita.")

            app_date = datetime.strptime(app_date_str, '%Y-%m-%d').date()
            app_time = datetime.strptime(app_time_str, '%H:%M').time()

            paciente = get_object_or_404(CustomerProfile, pk=patient_id)
            servicio = get_object_or_404(Service, pk=service_id)
            enfermero = get_object_or_404(User, pk=nurse_id, rol='enfermero')
            selected_status = get_object_or_404(AppointmentStatus, pk=status_id) # <-- OBTENER ESTADO POR ID

            producto = None # Inicializar
            if producto_id: # Solo buscar si se envió un producto_id
                producto = Product.objects.filter(id=producto_id).first()

            # --- Determinar Ubicación ---
            ubicacion_cita = ""
            mapa_cita = ""
            if tipo_ubicacion == 'domicilio':
                if not paciente.direccion: # Solo la dirección es estrictamente necesaria para copiar
                     raise ValueError("El paciente no tiene dirección registrada para cita a domicilio.")
                ubicacion_cita = paciente.direccion
                mapa_cita = paciente.ubicacion_mapa or "" # Puede ser None o vacío
            elif tipo_ubicacion == 'otro':
                if not ubicacion_manual: # Solo la ubicación es estrictamente necesaria
                     raise ValueError("Se requiere la dirección para el tipo 'otra ubicación'.")
                ubicacion_cita = ubicacion_manual
                mapa_cita = mapa_manual or ""
            else:
                 raise ValueError("Tipo de ubicación inválido.")

            # --- Encontrar Schedule para Aplicación ---
            try:
                app_schedule = Schedule.objects.get(
                    enfermero=enfermero,
                    fecha=app_date,
                    hora_inicio__lte=app_time,
                    hora_fin__gt=app_time, # gt porque la cita empieza a esa hora
                    disponible=True
                )
            except Schedule.DoesNotExist:
                 raise ValueError(f"No hay horario de trabajo definido para el enfermero {enfermero.nombres} en {app_date} a las {app_time}.")

            # --- Validar Conflicto para Aplicación ---
            # (Considera la duración del servicio si es variable)
            app_conflict = Appointment.objects.filter(
                enfermero=enfermero, fecha=app_date, hora=app_time
            ).exists()
            if app_conflict:
                 raise ValueError(f"Conflicto: Ya existe una cita para el enfermero {enfermero.nombres} en {app_date} a las {app_time}.")

            # 2. Crear Cita de Aplicación
            appointment_app = Appointment.objects.create(
                paciente=paciente,
                servicio=servicio,
                enfermero=enfermero,
                horario=app_schedule,
                fecha=app_date,
                hora=app_time,
                tipo_ubicacion=tipo_ubicacion,
                ubicacion=ubicacion_cita,
                mapa_ubicacion=mapa_cita,
                estado=selected_status, # <-- USAR ESTADO SELECCIONADO
                asignado_por=request.user,
                producto=producto,
                notas=notas_cita,
                doctor_name=doctor_name_cita,
            )

            # 3. Crear Cita de Retiro (si aplica)
            if servicio.requires_removal and requires_removal: # verifica el flag del modelo y el input del form
                if not rem_date_str or not rem_time_str:
                    raise ValueError("Faltan fecha/hora para la cita de retiro.")

                rem_date = datetime.strptime(rem_date_str, '%Y-%m-%d').date()
                rem_time = datetime.strptime(rem_time_str, '%H:%M').time()

                if datetime.combine(rem_date, rem_time) <= datetime.combine(app_date, app_time):
                     raise ValueError("La hora de retiro debe ser posterior a la de aplicación.")

                try:
                    rem_schedule = Schedule.objects.get(
                        enfermero=enfermero,
                        fecha=rem_date,
                        hora_inicio__lte=rem_time,
                        hora_fin__gt=rem_time,
                        disponible=True
                    )
                except Schedule.DoesNotExist:
                     raise ValueError(f"El enfermero {enfermero.nombres} no tiene horario de trabajo definido para el retiro en {rem_date} a las {rem_time}.")

                rem_conflict = Appointment.objects.filter(
                    enfermero=enfermero, fecha=rem_date, hora=rem_time
                ).exists()
                if rem_conflict:
                     raise ValueError(f"Conflicto: Ya existe una cita para el enfermero {enfermero.nombres} en {rem_date} a las {rem_time} (retiro).")

                Appointment.objects.create(
                    paciente=paciente,
                    servicio=servicio, # Podrías tener un servicio específico para "Retiro"
                    enfermero=enfermero,
                    horario=rem_schedule,
                    fecha=rem_date,
                    hora=rem_time,
                    tipo_ubicacion=tipo_ubicacion, # Asume misma ubicación
                    ubicacion=ubicacion_cita,
                    mapa_ubicacion=mapa_cita,
                    estado=selected_status, # Asume mismo estado inicial para retiro
                    asignado_por=request.user,
                    notas=f"CITA DE RETIRO (Aplicación original: {app_date_str} {app_time_str}). {notas_cita}",
                )

            return JsonResponse({'status': 'success', 'message': 'Cita(s) creada(s) exitosamente.'})

        except (ValueError, json.JSONDecodeError) as e: # ValueError para nuestras validaciones
             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        # Captura explícita de DoesNotExist para cada get_object_or_404 (ya lo hace Django, pero por claridad)
        except CustomerProfile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paciente no encontrado.'}, status=404)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Servicio no encontrado.'}, status=404)
        except User.DoesNotExist: # Específicamente para el enfermero
            return JsonResponse({'status': 'error', 'message': 'Enfermero no encontrado.'}, status=404)
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Estado de cita seleccionado no es válido.'}, status=404)
        except Exception as e:
            print(f"Error interno en POST /citas/callcenter/crear/: {type(e).__name__} - {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': 'Ocurrió un error interno inesperado. Revise los logs del servidor.'}, status=500)
