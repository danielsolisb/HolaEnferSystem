from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment-list'),
    path('nuevo/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/detalle/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<int:pk>/editar/', views.AppointmentUpdateView.as_view(), name='appointment-update'),
    path('<int:pk>/eliminar/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('horarios/nuevo/', views.ScheduleCreateView.as_view(), name='nuevo-horario'),
    path('horarios/mis-horarios/', views.ScheduleListView.as_view(), name='mis-horarios'),
    path('horarios/editar/<int:pk>/', views.ScheduleUpdateView.as_view(), name='editar-horario'),
    path('horarios/eliminar/<int:pk>/', views.ScheduleDeleteView.as_view(), name='eliminar-horario'),
    path('api/pacientes/', views.obtener_pacientes_por_ciudad, name='api-obtener-pacientes'),
    path('api/horarios/', views.obtener_horarios_por_enfermero, name='api-obtener-horarios'),



]

