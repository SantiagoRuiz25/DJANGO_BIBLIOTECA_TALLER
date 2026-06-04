from rest_framework.permissions import BasePermission

ADMINISTRADOR = 'Administrador'
BIBLIOTECARIO = 'Bibliotecario'


def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


class IsAdministrador(BasePermission):
    """Solo usuarios del grupo Administrador."""
    message = "Solo los administradores pueden realizar esta acción."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            user_in_group(request.user, ADMINISTRADOR) or request.user.is_superuser
        )


class IsBibliotecario(BasePermission):
    """Usuarios del grupo Bibliotecario (sin delete)."""
    message = "No tiene permisos para realizar esta acción."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser or user_in_group(request.user, ADMINISTRADOR):
            return True
        if user_in_group(request.user, BIBLIOTECARIO):
            # Bibliotecario NO puede eliminar
            if view.action == 'destroy':
                self.message = "Los bibliotecarios no tienen permisos de eliminación."
                return False
            return True
        return False
