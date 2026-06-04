import logging

logger = logging.getLogger('biblioteca')

LOGGED_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}


class LoggingMiddleware:
    """Registra en logs/api.log las operaciones POST, PUT, PATCH, DELETE."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        method = request.method.upper()
        if method in LOGGED_METHODS:
            user = request.user.username if request.user.is_authenticated else 'anonymous'
            logger.info(
                f"[{method}] path={request.path} | user={user} | status={response.status_code}"
            )

        return response
