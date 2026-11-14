from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

PERMISOS_EMPLEADO = {
    "catalogo": {
        "categoria": ["add", "change", "delete", "view"],
        "producto": ["add", "change", "delete", "view"],
    },
    "pedidos": {
        "pedido": ["view", "change"],
        "detallepedido": ["view"],
    },
}


class Command(BaseCommand):
    help = "Crea el grupo Empleado con sus permisos."

    def handle(self, *args, **options):
        grupo, _ = Group.objects.get_or_create(name="Empleado")

        permisos = []
        for app, modelos in PERMISOS_EMPLEADO.items():
            for modelo, acciones in modelos.items():
                for accion in acciones:
                    permisos.append(
                        Permission.objects.get(
                            content_type__app_label=app,
                            codename=f"{accion}_{modelo}",
                        )
                    )
        grupo.permissions.set(permisos)
        self.stdout.write(self.style.SUCCESS(
            f"Grupo «Empleado» listo con {len(permisos)} permisos."
        ))