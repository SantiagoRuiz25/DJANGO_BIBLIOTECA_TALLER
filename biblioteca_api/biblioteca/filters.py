import django_filters
from .models import Libro, Usuario, Prestamo, Autor, Categoria, Editorial, Devolucion, Multa


class LibroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    categoria = django_filters.NumberFilter(field_name='categoria__id')
    autor = django_filters.NumberFilter(field_name='autor__id')
    editorial = django_filters.NumberFilter(field_name='editorial__id')
    anio_publicacion = django_filters.NumberFilter()

    class Meta:
        model = Libro
        fields = ['titulo', 'categoria', 'autor', 'editorial', 'anio_publicacion', 'activo']


class UsuarioFilter(django_filters.FilterSet):
    documento = django_filters.CharFilter(lookup_expr='icontains')
    correo = django_filters.CharFilter(lookup_expr='icontains')
    nombres = django_filters.CharFilter(lookup_expr='icontains')
    apellidos = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Usuario
        fields = ['documento', 'correo', 'nombres', 'apellidos', 'activo']


class PrestamoFilter(django_filters.FilterSet):
    usuario = django_filters.NumberFilter(field_name='usuario__id')
    libro = django_filters.NumberFilter(field_name='libro__id')
    fecha_prestamo = django_filters.DateFilter()
    fecha_limite = django_filters.DateFilter()

    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro', 'fecha_prestamo', 'fecha_limite', 'activo']


class AutorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    nacionalidad = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Autor
        fields = ['nombre', 'nacionalidad', 'activo']


class CategoriaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Categoria
        fields = ['nombre', 'activo']


class EditorialFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Editorial
        fields = ['nombre', 'activo']


class DevolucionFilter(django_filters.FilterSet):
    prestamo = django_filters.NumberFilter(field_name='prestamo__id')
    fecha_devolucion = django_filters.DateFilter()

    class Meta:
        model = Devolucion
        fields = ['prestamo', 'fecha_devolucion', 'activo']


class MultaFilter(django_filters.FilterSet):
    usuario = django_filters.NumberFilter(field_name='usuario__id')
    pagada = django_filters.BooleanFilter()

    class Meta:
        model = Multa
        fields = ['usuario', 'pagada', 'activo']
