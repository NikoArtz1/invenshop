from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    use_in_migrations: True
    
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("El email es obligatorio")
        user = self.model(email = self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    
    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("rol", "ADMIN")
        return self.create_user(email, password, **extra)
    
    
class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        EMPLEADO = "EMPLEADO", "Empleado"
        CLIENTE = "CLIENTE", "Cliente"
        
    username = None
    email = models.EmailField(unique = True)
    telefono = models.CharField(max_length=30, blank=True)
    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.CLIENTE)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UsuarioManager()

    @property
    def es_personal(self):
       return self.rol in (self.Rol.ADMIN, self.Rol.EMPLEADO)