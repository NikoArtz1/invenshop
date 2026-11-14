from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
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

    def save(self, *args, **kwargs):
        self.is_staff = self.rol in (self.Rol.ADMIN, self.Rol.EMPLEADO)
        self.is_superuser = self.rol == self.Rol.ADMIN
        super().save(*args, **kwargs)
        if kwargs.get("update_fields") is None:
            self._sincronizar_grupo()
    
    def _sincronizar_grupo(self):
        grupo = Group.objects.filter(name="Empleado").first()
        if grupo is None:
            return
        if self.rol == self.Rol.EMPLEADO:
            self.groups.add(grupo)
        else:
            self.groups.remove(grupo)