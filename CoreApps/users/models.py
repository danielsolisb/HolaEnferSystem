from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from CoreApps.core.models import City

class UserManager(BaseUserManager):
    """
    Gestor personalizado para el modelo de usuario donde el email es el identificador único
    en lugar del nombre de usuario.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el email y contraseña proporcionados.
        """
        if not email:
            raise ValueError(_('El Email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el email y contraseña proporcionados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('rol', 'operador')  # Por defecto, los superusuarios son operadores

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Modelo de usuario personalizado donde el email es el identificador único
    para autenticación en lugar del nombre de usuario.
    """
    ROL_CHOICES = (
        ('enfermero', 'Enfermero'),
        ('operador', 'Operador'),
        ('administrador', 'Administrador'),
    )
    
    username = None  # Eliminamos el campo username
    email = models.EmailField(_('correo electrónico'), unique=True)
    cedula = models.CharField(_('cédula'), max_length=20, unique=True)
    nombres = models.CharField(_('nombres completos'), max_length=100)
    telefono = models.CharField(_('número de teléfono'), max_length=20, blank=True)
    rol = models.CharField(_('rol'), max_length=20, choices=ROL_CHOICES, default='enfermero')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name=_('foto de perfil'))
    ciudad = models.ForeignKey(City, on_delete=models.PROTECT, related_name='usuarios', blank=True, null=True) # <-- nuevo campo
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cedula', 'nombres', 'rol']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
    
    def get_full_name(self):
        """
        Retorna el nombre completo del usuario.
        """
        return self.nombres
        
    def __str__(self):
        return self.email
