from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report-list'),
    path('crear/', views.ReportCreateView.as_view(), name='report-create'),
    path('<int:pk>/detalle/', views.ReportDetailView.as_view(), name='report-detail'),
    path('<int:pk>/editar/', views.ReportUpdateView.as_view(), name='report-update'),
    path('<int:pk>/eliminar/', views.ReportDeleteView.as_view(), name='report-delete'),
    path('adjuntar-documento/', views.ConsentOrPrescriptionCreateView.as_view(), name='consent-or-prescription-create'),

]
