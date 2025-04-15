from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserAdmin(UserAdmin):
    """
    Panel de administración actualizado con todos los campos del usuario personalizado.
    """
    model = User
    list_display = ('email', 'cedula', 'nombres', 'telefono', 'rol', 'is_staff', 'is_active', 'profile_image_display')
    list_filter = ('rol', 'is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('cedula', 'nombres', 'telefono', 'rol', 'profile_image')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'cedula', 'nombres', 'telefono', 'rol', 'profile_image', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    search_fields = ('email', 'cedula', 'nombres')
    ordering = ('email',)

    def profile_image_display(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="50" height="50" style="border-radius:50%;"/>'
        return "Sin Imagen"
    
    profile_image_display.short_description = 'Foto de perfil'
    profile_image_display.allow_tags = True

admin.site.register(User, CustomUserAdmin)
