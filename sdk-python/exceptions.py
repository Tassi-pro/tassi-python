"""Exceptions personnalisées du SDK."""


class MonSDKException(Exception):
    """Exception de base du SDK."""
    pass


class AuthenticationError(MonSDKException):
    """Erreur d'authentification."""
    pass


class ValidationError(MonSDKException):
    """Erreur de validation des données."""
    pass


class RateLimitError(MonSDKException):
    """Erreur de limite de taux."""
    pass


class NotFoundError(MonSDKException):
    """Ressource non trouvée."""
    pass