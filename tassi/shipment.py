"""Ressource Shipment"""
from .resource import Resource


class Shipment(Resource):
    """Gestion des expéditions"""

    @classmethod
    def create(cls, params=None, headers=None):
        """Crée une expédition"""
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        return cls._create(params, headers)