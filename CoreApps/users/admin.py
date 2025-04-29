from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form     = CustomUserChangeForm

    list_display = (
        'email','cedula','nombres','rol',
        'ciudad','display_zonas',
        'profile_image_display','is_staff','is_active'
    )
    list_filter = ('rol','ciudad','zonas','is_staff','is_active')
    filter_horizontal = ('groups','user_permissions','zonas')

    # Volvemos a incluir todos los bloques originales, añadiendo 'zonas' donde toca
    fieldsets = (
        (None, {'fields': ('email','password')}),
        (_('Información personal'), {
            'fields': (
                'cedula','nombres','telefono',
                'rol','profile_image',
                'ciudad','zonas'
            )
        }),
        (_('Permisos'), {
            'fields': (
                'is_active','is_staff','is_superuser',
                'groups','user_permissions'
            )
        }),
        (_('Fechas importantes'), {
            'fields': ('last_login','date_joined')
        }),
    )

    # Para crear usuarios: email+password primero, luego info personal, luego permisos
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1','password2'),
        }),
        (_('Información personal'), {
            'fields': (
                'cedula','nombres','telefono',
                'rol','profile_image',
                'ciudad','zonas',
            )
        }),
        (_('Permisos'), {
            'fields': (
                'is_active','is_staff','is_superuser',
                'groups','user_permissions'
            )
        }),
    )

    search_fields = ('email','cedula','nombres','ciudad__nombre')
    ordering = ('email',)

    def display_zonas(self, obj):
        return ", ".join(z.nombre for z in obj.zonas.all())
    display_zonas.short_description = 'Zonas'

    def profile_image_display(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="50" height="50" ' \
                   f'style="border-radius:50%;object-fit:cover;"/>'
        return "Sin Imagen"
    profile_image_display.short_description = 'Foto de perfil'
    profile_image_display.allow_tags = True
