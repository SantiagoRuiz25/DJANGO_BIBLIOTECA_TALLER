from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from biblioteca.models import Autor, Categoria, Editorial, Usuario, Libro, Prestamo, Devolucion, Multa


MODELS = [Autor, Categoria, Editorial, Usuario, Libro, Prestamo, Devolucion, Multa]


class Command(BaseCommand):
    help = 'Crea los grupos Administrador y Bibliotecario con sus permisos'

    def handle(self, *args, **options):
        # Grupo Administrador - CRUD completo
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        bibliotecario_group, created2 = Group.objects.get_or_create(name='Bibliotecario')

        all_perms = []
        read_create_update_perms = []

        for model in MODELS:
            ct = ContentType.objects.get_for_model(model)
            for action in ['add', 'change', 'delete', 'view']:
                perm = Permission.objects.filter(content_type=ct, codename=f'{action}_{model.__name__.lower()}').first()
                if perm:
                    all_perms.append(perm)
                    if action != 'delete':
                        read_create_update_perms.append(perm)

        admin_group.permissions.set(all_perms)
        bibliotecario_group.permissions.set(read_create_update_perms)

        self.stdout.write(self.style.SUCCESS('✅ Grupo "Administrador" creado con CRUD completo'))
        self.stdout.write(self.style.SUCCESS('✅ Grupo "Bibliotecario" creado (sin permisos de eliminación)'))

        # Superusuario de prueba
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@biblioteca.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Superusuario "admin" creado (password: admin123)'))
        else:
            self.stdout.write('ℹ️  El usuario "admin" ya existe')
