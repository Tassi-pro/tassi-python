"""Gestionnaire des requêtes HTTP"""
import requests
from .tassi import Tassi
from .error import ApiConnectionError


class Requestor:
    SANDBOX_BASE = 'https://tassi-api.exanora.com'
    LIVE_BASE = 'https://tassi-api.exanora.com'  # Même URL pour le moment

    def __init__(self):
        self.session = requests.Session()

    def request(self, method, path, params=None, headers=None):
        """Effectue une requête HTTP"""
        url = self._url(path)
        request_headers = {**self._default_headers(), **(headers or {})}

        try:
            if method.upper() in ['GET', 'HEAD', 'DELETE']:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    headers=request_headers,
                    verify=Tassi.get_verify_ssl_certs()
                )
            else:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=params,
                    headers=request_headers,
                    verify=Tassi.get_verify_ssl_certs()
                )

            response.raise_for_status()

            return {
                'data': response.json() if response.content else {},
                'options': {
                    'environment': Tassi.get_environment()
                }
            }
        except requests.exceptions.RequestException as e:
            self._handle_request_exception(e)

    def _base_url(self):
        """Retourne l'URL de base"""
        api_base = Tassi.get_api_base()
        environment = Tassi.get_environment()

        if api_base:
            return api_base

        if environment in ['live']:
            return self.LIVE_BASE
        else:  # sandbox par défaut
            return self.SANDBOX_BASE

    def _url(self, path=''):
        """Construit l'URL complète"""
        return f"{self._base_url()}{path}"

    def _default_headers(self):
        """Retourne les headers par défaut"""
        api_key = Tassi.get_api_key()

        return {
            'X-Version': Tassi.VERSION,
            'X-Source': 'Tassi PythonLib',
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _handle_request_exception(self, e):
        """Gère les exceptions de requête"""
        message = f"Request error: {str(e)}"
        http_status = e.response.status_code if hasattr(e, 'response') and e.response else None
        http_request = e.request if hasattr(e, 'request') else None
        http_response = e.response if hasattr(e, 'response') else None

        raise ApiConnectionError(
            message,
            http_status=http_status,
            http_request=http_request,
            http_response=http_response
        )