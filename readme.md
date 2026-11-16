# InvenShop

Programación IV - ITSE - 2026

## Integrantes
- Bravo Gabriel Martin
- Exequiel Montoya Fernando
- Ledesma Moyano Tomas
- Elba Maria Juan Cruz

## Instalación
```bash
git clone <url-del-repositorio>
cd invenshop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto con:

```
SECRET_KEY=una-clave-larga-y-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Luego:

```bash
python manage.py migrate
python manage.py crear_roles
python manage.py createsuperuser
python manage.py runserver
```

La aplicación queda disponible en http://127.0.0.1:8000/ y el panel de administración en /admin/.

## Apps
- `usuarios`: modelo de usuario personalizado (login por email), registro, perfil y roles.
- `catalogo`: categorías y productos, listado con filtros y paginación.
- `pedidos`: carrito en sesión, checkout, historial y estados de los pedidos.

## Roles
| Rol | Permisos |
|---|---|
| Administrador | Acceso total: usuarios y roles, catálogo, pedidos |
| Empleado | Productos, categorías, stock y estado de pedidos. Sin gestión de usuarios |
| Cliente | Catálogo, carrito, pedidos propios y edición de su perfil |

El registro público siempre crea usuarios con rol Cliente. El rol de un usuario se cambia desde el admin (sección Usuarios).
