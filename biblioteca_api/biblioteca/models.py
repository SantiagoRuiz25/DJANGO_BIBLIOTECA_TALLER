from django.db import models


# ==========================================
# MODELO BASE ABSTRACTO (Auditoría)
# ==========================================
class BaseModel(models.Model):
    activo = models.BooleanField(default=True)
    usuario_creacion = models.CharField(max_length=150, null=True, blank=True)
    usuario_modificacion = models.CharField(max_length=150, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ==========================================
# AUTORES
# ==========================================
class Autor(BaseModel):
    nombre = models.CharField(max_length=200)
    nacionalidad = models.CharField(max_length=100, null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '"biblioteca"."autores"'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# ==========================================
# CATEGORIAS
# ==========================================
class Categoria(BaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '"biblioteca"."categorias"'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# ==========================================
# EDITORIALES
# ==========================================
class Editorial(BaseModel):
    nombre = models.CharField(max_length=200)
    direccion = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = '"biblioteca"."editoriales"'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# ==========================================
# USUARIOS
# ==========================================
class Usuario(BaseModel):
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    documento = models.CharField(max_length=30, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = '"biblioteca"."usuarios"'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


# ==========================================
# LIBROS
# ==========================================
class Libro(BaseModel):
    titulo = models.CharField(max_length=300)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    anio_publicacion = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name='libros')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='libros')
    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT, related_name='libros')

    class Meta:
        db_table = '"biblioteca"."libros"'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


# ==========================================
# PRESTAMOS
# ==========================================
class Prestamo(BaseModel):
    fecha_prestamo = models.DateField()
    fecha_limite = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='prestamos')

    class Meta:
        db_table = '"biblioteca"."prestamos"'
        ordering = ['-fecha_prestamo']

    def __str__(self):
        return f"Préstamo #{self.pk} - {self.usuario} / {self.libro}"


# ==========================================
# DEVOLUCIONES
# ==========================================
class Devolucion(BaseModel):
    fecha_devolucion = models.DateField()
    observaciones = models.TextField(null=True, blank=True)
    prestamo = models.OneToOneField(Prestamo, on_delete=models.PROTECT, related_name='devolucion')

    class Meta:
        db_table = '"biblioteca"."devoluciones"'
        ordering = ['-fecha_devolucion']

    def __str__(self):
        return f"Devolución #{self.pk} - Préstamo #{self.prestamo_id}"


# ==========================================
# MULTAS
# ==========================================
class Multa(BaseModel):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=300)
    pagada = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='multas')

    class Meta:
        db_table = '"biblioteca"."multas"'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Multa #{self.pk} - {self.usuario} / ${self.valor}"
