from rest_framework import serializers
from .models import Autor, Categoria, Editorial, Usuario, Libro, Prestamo, Devolucion, Multa


# ==========================================
# MIXIN DE AUDITORÍA (reutilizable)
# Replica exactamente la lógica de api_empresa
# ==========================================
class AuditMixin:
    """
    Aplica la auditoría automática:
    - POST: usuario_modificacion es read_only
    - PUT/PATCH: usuario_creacion es read_only, usuario_modificacion requerido
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            if request.method == 'POST':
                if 'usuario_modificacion' in self.fields:
                    self.fields['usuario_modificacion'].read_only = True
            elif request.method in ['PUT', 'PATCH']:
                if 'usuario_creacion' in self.fields:
                    self.fields['usuario_creacion'].read_only = True
                if 'usuario_modificacion' in self.fields:
                    self.fields['usuario_modificacion'].required = True


# ==========================================
# SERIALIZERS ANIDADOS (Nested - solo lectura)
# ==========================================
class AutorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad']


class CategoriaNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class EditorialNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id', 'nombre']


class UsuarioNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombres', 'apellidos', 'documento']


class LibroNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'isbn']


# ==========================================
# AUTOR
# ==========================================
class AutorSerializer(AuditMixin, serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


# ==========================================
# CATEGORIA
# ==========================================
class CategoriaSerializer(AuditMixin, serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


# ==========================================
# EDITORIAL
# ==========================================
class EditorialSerializer(AuditMixin, serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = '__all__'


# ==========================================
# USUARIO
# ==========================================
class UsuarioSerializer(AuditMixin, serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


# ==========================================
# LIBRO (con nested serializers de lectura)
# ==========================================
class LibroSerializer(AuditMixin, serializers.ModelSerializer):
    # Nested (solo lectura)
    autor_detalle = AutorNestedSerializer(source='autor', read_only=True)
    categoria_detalle = CategoriaNestedSerializer(source='categoria', read_only=True)
    editorial_detalle = EditorialNestedSerializer(source='editorial', read_only=True)

    # IDs para escritura
    autor = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.filter(activo=True))
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.filter(activo=True))
    editorial = serializers.PrimaryKeyRelatedField(queryset=Editorial.objects.filter(activo=True))

    class Meta:
        model = Libro
        fields = [
            'id', 'titulo', 'isbn', 'anio_publicacion', 'stock',
            'autor', 'autor_detalle',
            'categoria', 'categoria_detalle',
            'editorial', 'editorial_detalle',
            'activo', 'usuario_creacion', 'usuario_modificacion',
            'fecha_creacion', 'fecha_modificacion',
        ]


# ==========================================
# PRESTAMO (con nested)
# ==========================================
class PrestamoSerializer(AuditMixin, serializers.ModelSerializer):
    usuario_detalle = UsuarioNestedSerializer(source='usuario', read_only=True)
    libro_detalle = LibroNestedSerializer(source='libro', read_only=True)

    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(activo=True))
    libro = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.filter(activo=True))

    class Meta:
        model = Prestamo
        fields = [
            'id', 'fecha_prestamo', 'fecha_limite',
            'usuario', 'usuario_detalle',
            'libro', 'libro_detalle',
            'activo', 'usuario_creacion', 'usuario_modificacion',
            'fecha_creacion', 'fecha_modificacion',
        ]


# ==========================================
# DEVOLUCION (con nested)
# ==========================================
class PrestamoResumenSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioNestedSerializer(source='usuario', read_only=True)
    libro_detalle = LibroNestedSerializer(source='libro', read_only=True)

    class Meta:
        model = Prestamo
        fields = ['id', 'fecha_prestamo', 'fecha_limite', 'usuario_detalle', 'libro_detalle']


class DevolucionSerializer(AuditMixin, serializers.ModelSerializer):
    prestamo_detalle = PrestamoResumenSerializer(source='prestamo', read_only=True)
    prestamo = serializers.PrimaryKeyRelatedField(queryset=Prestamo.objects.filter(activo=True))

    class Meta:
        model = Devolucion
        fields = [
            'id', 'fecha_devolucion', 'observaciones',
            'prestamo', 'prestamo_detalle',
            'activo', 'usuario_creacion', 'usuario_modificacion',
            'fecha_creacion', 'fecha_modificacion',
        ]


# ==========================================
# MULTA (con nested)
# ==========================================
class MultaSerializer(AuditMixin, serializers.ModelSerializer):
    usuario_detalle = UsuarioNestedSerializer(source='usuario', read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(activo=True))

    class Meta:
        model = Multa
        fields = [
            'id', 'valor', 'motivo', 'pagada',
            'usuario', 'usuario_detalle',
            'activo', 'usuario_creacion', 'usuario_modificacion',
            'fecha_creacion', 'fecha_modificacion',
        ]
