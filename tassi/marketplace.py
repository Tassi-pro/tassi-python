"""Ressource Marketplace"""
from .resource import Resource
from .util import array_to_tassi_object


class Marketplace(Resource):
    """Gestion des marketplaces"""

    @classmethod
    def retrieve(cls, id, headers=None):
        """Récupère une marketplace"""
        if headers is None:
            headers = {}
        return cls._retrieve(id, headers)

    @classmethod
    def update(cls, id, params=None, headers=None):
        """Met à jour une marketplace"""
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        return cls._update(id, params, headers)

    def save(self, headers=None):
        """Sauvegarde la marketplace"""
        if headers is None:
            headers = {}
        return self._save(headers)

    def get_wallet_history(self, params=None, headers=None):
        """Récupère l'historique du wallet"""
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        url = f"{self.instance_url()}/wallet_history"

        response = self.__class__._static_request('get', url, params, headers)
        return array_to_tassi_object(response['data'], response['options'])