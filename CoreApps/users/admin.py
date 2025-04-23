from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'email', 'cedula', 'nombres', 'rol', 'ciudad', 
        'profile_image_display', 'is_staff', 'is_active'
    )
    list_filter = ('rol', 'ciudad', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {
            'fields': ('cedula', 'nombres', 'telefono', 'rol', 'profile_image', 'ciudad')
        }),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Fechas importantes'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'cedula', 'nombres', 'telefono', 'rol', 
                'profile_image', 'ciudad', 'password1', 'password2', 
                'is_staff', 'is_active'
            ),
        }),
    )

    search_fields = ('email', 'cedula', 'nombres', 'ciudad__nombre')
    ordering = ('email',)

    def profile_image_display(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="50" height="50" style="border-radius:50%; object-fit: cover;"/>'
        return "Sin Imagen"
    
    profile_image_display.short_description = 'Foto de perfil'
    profile_image_display.allow_tags = True
