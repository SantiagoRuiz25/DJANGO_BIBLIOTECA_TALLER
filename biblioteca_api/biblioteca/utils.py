from rest_framework.response import Response
from rest_framework import status


def success_response(message="Operación realizada correctamente", data=None, status_code=status.HTTP_200_OK):
    """Respuesta JSON estandarizada para operaciones exitosas."""
    return Response(
        {
            "success": True,
            "message": message,
            "data": data if data is not None else {},
        },
        status=status_code,
    )


def error_response(message="Ha ocurrido un error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """Respuesta JSON estandarizada para errores."""
    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors if errors is not None else {},
        },
        status=status_code,
    )


def created_response(message="Registro creado correctamente", data=None):
    return success_response(message=message, data=data, status_code=status.HTTP_201_CREATED)


def not_found_response(message="Registro no encontrado"):
    return error_response(message=message, status_code=status.HTTP_404_NOT_FOUND)


def unauthorized_response(message="No autorizado"):
    return error_response(message=message, status_code=status.HTTP_401_UNAUTHORIZED)
