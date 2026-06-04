from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AutorViewSet, CategoriaViewSet, EditorialViewSet, 
    UsuarioViewSet, LibroViewSet, PrestamoViewSet, 
    DevolucionViewSet, MultaViewSet
)

router = DefaultRouter()
router.register(r'autores', AutorViewSet, basename='autores')
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'editoriales', EditorialViewSet, basename='editoriales')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'libros', LibroViewSet, basename='libros')
router.register(r'prestamos', PrestamoViewSet, basename='prestamos')
router.register(r'devoluciones', DevolucionViewSet, basename='devoluciones')
router.register(r'multas', MultaViewSet, basename='multas')

urlpatterns = [
    path('', include(router.urls)),
]