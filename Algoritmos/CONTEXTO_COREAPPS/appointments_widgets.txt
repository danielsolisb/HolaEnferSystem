from django.urls import reverse
from django_select2.forms import ModelSelect2Widget
from CoreApps.customers.models import CustomerProfile

class CustomerByCityWidget(ModelSelect2Widget):
    model = CustomerProfile
    search_fields = ['nombres__icontains', 'apellidos__icontains']
    dependent_fields = {'ciudad': 'ciudad'}

    def label_from_instance(self, obj):
        return f"{obj.nombres} {obj.apellidos} ({obj.cedula})"

    def get_url(self):
        return reverse('appointments:paciente-autocomplete')
