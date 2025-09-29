"""Ressource Package"""
from .resource import Resource
from .util import array_to_tassi_object


class Package(Resource):
    """Gestion des packages"""

    @classmethod
    def retrieve(cls, id, headers=None):
        """Récupère un package"""
        if headers is None:
            headers = {}
        return cls._retrieve(id, headers)

    @classmethod
    def all(cls, params=None, headers=None):
        """Liste tous les packages"""
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        return cls._all(params, headers)

    @classmethod
    def update(cls, id, params=None, headers=None):
        """Met à jour un package"""
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        return cls._update(id, params, headers)

    def save(self, headers=None):
        """Sauvegarde le package"""
        if headers is None:
            headers = {}
        return self._save(headers)

    def track(self, headers=None):
        """Suivi du package"""
        if headers is None:
            headers = {}

        url = f"{self.instance_url()}/track"

        response = self.__class__._static_request('get', url, {}, headers)
        return array_to_tassi_object(response['data'], response['options'])

    def get_shipping_label(self, label_id, headers=None):
        """Récupère l'étiquette d'expédition"""
        if headers is None:
            headers = {}

        url = f"{self.instance_url()}/shipping_labels/{label_id}"

        response = self.__class__._static_request('get', url, {}, headers)
        return array_to_tassi_object(response['data'], response['options'])