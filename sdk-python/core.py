"""Module principal du SDK."""

import json
import requests
from typing import Dict, Any, Optional
from .exceptions import MonSDKException


class MonSDK:
    """Classe principale du SDK."""

    BASE_URL = "https://api.example.com"
    SANDBOX_URL = "https://api-sandbox.example.com"

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        sandbox: bool = False,
        timeout: int = 30
    ):
        """
        Initialise le client SDK.

        Args:
            api_key: Clé API publique
            secret_key: Clé secrète
            sandbox: Utiliser l'environnement de test
            timeout: Timeout des requêtes HTTP
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.sandbox = sandbox
        self.timeout = timeout

        self.base_url = self.SANDBOX_URL if sandbox else self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-Secret-Key": self.secret_key,
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Effectue une requête HTTP.

        Args:
            method: Méthode HTTP (GET, POST, etc.)
            endpoint: Point de terminaison de l'API
            data: Données à envoyer
            params: Paramètres de requête

        Returns:
            Réponse JSON de l'API

        Raises:
            MonSDKException: En cas d'erreur
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise MonSDKException(f"Erreur de requête: {str(e)}")
        except json.JSONDecodeError as e:
            raise MonSDKException(f"Erreur de décodage JSON: {str(e)}")

    def get_status(self, resource_id: str) -> Dict[str, Any]:
        """
        Récupère le statut d'une ressource.

        Args:
            resource_id: ID de la ressource

        Returns:
            Informations sur la ressource
        """
        return self._make_request("GET", f"/status/{resource_id}")

    def create_resource(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée une nouvelle ressource.

        Args:
            data: Données de la ressource

        Returns:
            Ressource créée
        """
        return self._make_request("POST", "/resources", data=data)