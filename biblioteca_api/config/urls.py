from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from biblioteca.views import CustomTokenObtainPairView, LogoutView

schema_view = get_schema_view(
    openapi.Info(
        title="API Sistema de Gestión de Biblioteca",
        default_version='v1',
        description="API REST completa para gestión de biblioteca: libros, autores, préstamos, devoluciones y más.",
        contact=openapi.Contact(email="admin@biblioteca.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Redirigir la raíz (/) directamente a la documentación de Swagger
    path('', RedirectView.as_view(url='swagger/', permanent=False), name='index'),

    path('admin/', admin.site.urls),

    # Swagger / ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # JWT Auth (Tus endpoints personalizados para producción)
    path('api/v1/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/logout/', LogoutView.as_view(), name='token_blacklist'),

    # API versionada (Apunta al router limpio de biblioteca.urls)
    path('api/v1/', include('biblioteca.urls')),

    # ESTA LÍNEA SE AGREGA AQUÍ ABAJO: Activa el Login visual de DRF en el navegador
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]