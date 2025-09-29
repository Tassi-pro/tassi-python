"""Classe de base pour toutes les ressources"""
from inflection import pluralize
from .tassi_object import TassiObject
from .requestor import Requestor
from .error import InvalidRequestError
from .util import array_to_tassi_object


class Resource(TassiObject):
    _requestor = None

    @classmethod
    def set_requestor(cls, req):
        """Définit le requestor"""
        cls._requestor = req

    @classmethod
    def get_requestor(cls):
        """Retourne le requestor"""
        if cls._requestor is None:
            cls._requestor = Requestor()
        return cls._requestor

    @classmethod
    def class_name(cls):
        """Retourne le nom de la classe"""
        return cls.__name__.lower()

    @classmethod
    def class_path(cls):
        """Retourne le chemin de la classe"""
        base = cls.class_name()
        plural = pluralize(base)
        return f"/{plural}"

    @classmethod
    def resource_path(cls, id):
        """Retourne le chemin de la ressource"""
        if id is None:
            klass = cls.class_name()
            raise InvalidRequestError(
                f"Could not determine which URL to request: {klass} instance has invalid ID: {id}"
            )

        base = cls.class_path()
        return f"{base}/{id}"

    def instance_url(self):
        """Retourne l'URL de l'instance"""
        return self.__class__.resource_path(self.id)

    @classmethod
    def _validate_params(cls, params=None):
        """Valide les paramètres"""
        if params is not None and not isinstance(params, dict):
            raise InvalidRequestError(
                'You must pass a dict as the first argument to Tassi API method calls.'
            )

    @classmethod
    def _static_request(cls, method, url, params=None, headers=None):
        """Effectue une requête statique"""
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        return cls.get_requestor().request(method, url, params, headers)

    @classmethod
    def _retrieve(cls, id, headers=None):
        """Récupère une ressource"""
        if headers is None:
            headers = {}

        url = cls.resource_path(id)
        class_name = cls.class_name()

        response = cls._static_request('get', url, None, headers)
        data = response['data']
        options = response['options']

        # Si la réponse contient la clé du nom de classe, l'utiliser
        if class_name in data:
            obj_data = data[class_name]
        else:
            obj_data = data

        obj = array_to_tassi_object(obj_data, options)
        return obj

    @classmethod
    def _all(cls, params=None, headers=None):
        """Liste toutes les ressources"""
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        cls._validate_params(params)
        path = cls.class_path()

        response = cls._static_request('get', path, params, headers)
        return array_to_tassi_object(response['data'], response['options'])

    @classmethod
    def _create(cls, params, headers=None):
        """Crée une ressource"""
        if headers is None:
            headers = {}

        cls._validate_params(params)
        url = cls.class_path()
        class_name = cls.class_name()

        response = cls._static_request('post', url, params, headers)
        data = response['data']
        options = response['options']

        # Si la réponse contient la clé du nom de classe, l'utiliser
        if class_name in data:
            obj_data = data[class_name]
        else:
            obj_data = data

        obj = array_to_tassi_object(obj_data, options)
        return obj

    @classmethod
    def _update(cls, id, params, headers=None):
        """Met à jour une ressource"""
        if headers is None:
            headers = {}

        cls._validate_params(params)
        url = cls.resource_path(id)
        class_name = cls.class_name()

        response = cls._static_request('put', url, params, headers)
        data = response['data']
        options = response['options']

        # Si la réponse contient la clé du nom de classe, l'utiliser
        if class_name in data:
            obj_data = data[class_name]
        else:
            obj_data = data

        obj = array_to_tassi_object(obj_data, options)
        return obj

    def _delete(self, headers=None):
        """Supprime une ressource"""
        if headers is None:
            headers = {}

        url = self.instance_url()
        self.__class__._static_request('delete', url, {}, headers)
        return self