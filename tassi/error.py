"""Exceptions personnalisées pour Tassi"""


class TassiError(Exception):
    """Exception de base"""
    pass


class InvalidRequestError(TassiError):
    """Erreur de requête invalide"""
    pass


class ApiConnectionError(TassiError):
    """Erreur de connexion à l'API"""

    def __init__(self, message, http_status=None, http_request=None, http_response=None):
        super().__init__(message)
        self.http_status = http_status
        self.http_request = http_request
        self.http_response = http_response


class AuthenticationError(TassiError):
    """Erreur d'authentification"""
    pass


class NotFoundError(TassiError):
    """Ressource non trouvée"""
    pass


class ValidationError(TassiError):
    """Erreur de validation"""
    pass