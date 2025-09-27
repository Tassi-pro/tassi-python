import json
import requests
from typing import Dict, Any, Optional, List
from .exceptions import (
    TassiException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
)


class Tassi:
    """Classe principale du SDK Tassi."""

    BASE_URL = "https://tassi-api.exanora.com"
    SANDBOX_URL = "https://sandbox-tassi-api.exanora.com"  # URL future pour sandbox

    def __init__(self, secret_key: str, sandbox: bool = False, timeout: int = 30):
        """
        Initialise le client Tassi.

        Args:
            secret_key: Clé secrète pour l'authentification
            sandbox: Utiliser l'environnement de test (future fonctionnalité)
            timeout: Timeout des requêtes HTTP en secondes
        """
        self.secret_key = secret_key
        self.sandbox = sandbox
        self.timeout = timeout

        self.base_url = self.SANDBOX_URL if sandbox else self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.secret_key}",
            }
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Effectue une requête HTTP vers l'API Tassi.

        Args:
            method: Méthode HTTP (GET, POST, PUT, DELETE)
            endpoint: Point de terminaison de l'API
            data: Données à envoyer dans le body
            params: Paramètres de requête URL

        Returns:
            Réponse JSON de l'API

        Raises:
            TassiException: En cas d'erreur générale
            AuthenticationError: En cas d'erreur d'authentification
            ValidationError: En cas d'erreur de validation
            NotFoundError: En cas de ressource non trouvée
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params,
                timeout=self.timeout,
            )

            if response.status_code == 401:
                raise AuthenticationError("Clé secrète invalide ou expirée")
            elif response.status_code == 404:
                raise NotFoundError("Ressource non trouvée")
            elif response.status_code == 422:
                raise ValidationError(f"Erreur de validation: {response.text}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise TassiException(f"Erreur de requête: {str(e)}")
        except json.JSONDecodeError as e:
            raise TassiException(f"Erreur de décodage JSON: {str(e)}")

    # Shipments
    def create_shipment(self, shipment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée un nouveau shipment.

        Args:
            shipment_data: Données du shipment selon le format API

        Returns:
            Shipment créé

        Example:
            shipment = {
                "shipment": {
                    "marketplace_id": "123",
                    "customer_id": "456",
                    "customer": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john@example.com",
                        "address": "123 Main St",
                        "city": "Cotonou",
                        "country_code": "BJ"
                    },
                    "pickup_point_id": "789",
                    "package": {
                        "description": "Electronics",
                        "weight": "2.5",
                        "dimensions": "20x15x10",
                        "declared_value": "100",
                        "currency": "XOF",
                        "insurance": False
                    },
                    "route": {
                        "origin": "Cotonou",
                        "destination": "Porto-Novo",
                        "stops": []
                    }
                }
            }
        """
        return self._make_request("POST", "/shipments", data=shipment_data)

    # Packages
    def list_packages(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère la liste des packages.

        Args:
            params: Paramètres de filtrage optionnels

        Returns:
            Liste des packages
        """
        return self._make_request("GET", "/packages", params=params)

    def get_package(self, package_id: str) -> Dict[str, Any]:
        """
        Récupère les détails d'un package.

        Args:
            package_id: ID du package

        Returns:
            Détails du package
        """
        return self._make_request("GET", f"/packages/{package_id}")

    def update_package(self, package_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Met à jour un package.

        Args:
            package_id: ID du package
            data: Données de mise à jour

        Returns:
            Package mis à jour

        Example:
            # data = {
            #     "status": "in_transit",
            #     "tracking_number": "TRK123456"
            # }
        """
        return self._make_request("PUT", f"/packages/{package_id}", data=data)

    def track_package(self, package_id: str) -> Dict[str, Any]:
        """
        Suit un package.

        Args:
            package_id: ID du package

        Returns:
            Informations de suivi
        """
        return self._make_request("GET", f"/packages/{package_id}/track")

    def get_shipping_label(self, package_id: str, label_id: str) -> Dict[str, Any]:
        """
        Récupère une étiquette d'expédition.

        Args:
            package_id: ID du package
            label_id: ID de l'étiquette

        Returns:
            Étiquette d'expédition
        """
        return self._make_request(
            "GET", f"/packages/{package_id}/shipping_labels/{label_id}"
        )

    # Carriers
    def get_carrier(
        self, carrier_id: str, include: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Récupère les détails d'un transporteur.

        Args:
            carrier_id: ID du transporteur
            include: Données supplémentaires à inclure

        Returns:
            Détails du transporteur
        """
        params = {"include": include} if include else None
        return self._make_request("GET", f"/carriers/{carrier_id}", params=params)

    def update_carrier(self, carrier_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Met à jour un transporteur.

        Args:
            carrier_id: ID du transporteur
            data: Données de mise à jour

        Returns:
            Transporteur mis à jour
        """
        return self._make_request("PUT", f"/carriers/{carrier_id}", data=data)

    # Marketplaces
    def get_marketplace(self, marketplace_id: str) -> Dict[str, Any]:
        """
        Récupère les détails d'une marketplace.

        Args:
            marketplace_id: ID de la marketplace

        Returns:
            Détails de la marketplace
        """
        return self._make_request("GET", f"/marketplaces/{marketplace_id}")

    def update_marketplace(
        self, marketplace_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Met à jour une marketplace.

        Args:
            marketplace_id: ID de la marketplace
            data: Données de mise à jour

        Returns:
            Marketplace mise à jour

        Example:
            data = {
                "name": "Market1",
                "api_name": "market1",
                "website": "market1.com",
                "email": "franckaigba4@gmail.com",
                "country_code": "BJ",
                "phone_number": "0163085267",
                "public_key": "",
                "secret_key": "",
                "is_active": False,
                "api_configuration": {}
            }
        """
        return self._make_request("PUT", f"/marketplaces/{marketplace_id}", data=data)

    def get_marketplace_wallet_history(
        self, marketplace_id: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Récupère l'historique du portefeuille d'une marketplace.

        Args:
            marketplace_id: ID de la marketplace
            params: Paramètres de pagination optionnels

        Returns:
            Historique du portefeuille

        Example response:
            {
                "wallet_movements": [],
                "meta": {
                    "current_page": 1,
                    "next_page": None,
                    "prev_page": None,
                    "per_page": 25,
                    "total_pages": 0,
                    "total_count": 0
                }
            }
        """
        return self._make_request(
            "GET", f"/marketplaces/{marketplace_id}/wallet_history", params=params
        )
