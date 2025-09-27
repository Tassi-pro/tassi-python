"""Exceptions personnalisées du SDK Tassi."""


class TassiException(Exception):
    """Exception de base du SDK Tassi."""

    pass


class AuthenticationError(TassiException):
    """Erreur d'authentification avec l'API Tassi."""

    pass


class ValidationError(TassiException):
    """Erreur de validation des données envoyées à l'API."""

    pass


class NotFoundError(TassiException):
    """Ressource non trouvée."""

    pass


class RateLimitError(TassiException):
    """Limite de taux dépassée."""

    pass
