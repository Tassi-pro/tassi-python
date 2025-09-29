"""
Class Tassi
Configuration principale pour l'API Tassi
"""


class Tassi:
    VERSION = '1.0.0'
    api_key = None
    api_base = None
    environment = 'sandbox'
    verify_ssl_certs = True

    @staticmethod
    def get_api_key():
        """Retourne l'API key"""
        return Tassi.api_key

    @staticmethod
    def set_api_key(api_key):
        """Définit l'API key"""
        Tassi.api_key = api_key

    @staticmethod
    def get_api_base():
        """Retourne l'API base"""
        return Tassi.api_base

    @staticmethod
    def set_api_base(api_base):
        """Définit l'API base"""
        Tassi.api_base = api_base

    @staticmethod
    def get_environment():
        """Retourne l'environnement"""
        return Tassi.environment

    @staticmethod
    def set_environment(environment):
        """Définit l'environnement"""
        Tassi.environment = environment

    @staticmethod
    def get_verify_ssl_certs():
        """Retourne si on vérifie les certificats SSL"""
        return Tassi.verify_ssl_certs

    @staticmethod
    def set_verify_ssl_certs(verify):
        """Définit si on vérifie les certificats SSL"""
        Tassi.verify_ssl_certs = verify