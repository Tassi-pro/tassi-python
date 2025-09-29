"""Tests pour la ressource Shipment"""
import pytest
import responses
from tassi import Tassi, Shipment
from tassi.error import ApiConnectionError


class TestShipment:
    """Tests pour Shipment"""

    def setup_method(self):
        """Configuration avant chaque test"""
        Tassi.set_api_key('test_api_key')
        Tassi.set_environment('sandbox')

    @responses.activate
    def test_create_complete(self):
        """Test de création avec payload complet"""
        payload = {
            "marketplace_id": "1",
            "customer_id": "",
            "customer": {
                "first_name": "Judicaël",
                "last_name": "DAKIN",
                "email": "marcellimsuanon@gmail.com",
                "address": "Rue 123, Houéyiho, Cotonou",
                "city": "Cotonou",
                "country_code": "BJ"
            },
            "pickup_point_id": "",
            "pickup_point": {
                "name": "Point Relais Houéyiho",
                "address": "Carrefour Houéyiho, Cotonou",
                "city": "Cotonou",
                "postal_code": "22901",
                "latitude": 6.3703,
                "longitude": 2.3912,
                "phone": "+22961020304",
                "email": "pickup.houeyiho@example.com",
                "is_active": True
            },
            "package": {
                "description": "Colis test contenant accessoires électroniques",
                "weight": 5,
                "dimensions": "10x10x10",
                "declared_value": "100",
                "currency": "USD",
                "insurance": False
            },
            "route": {
                "origin": "Cotonou",
                "destination": "Porto-Novo",
                "stops": [
                    {
                        "city": "Sèmè-Kpodji",
                        "address": "Avenue de l'Inter, Sèmè-Kpodji",
                        "latitude": 6.3512,
                        "longitude": 2.4987
                    }
                ]
            }
        }

        mock_response = {
            "shipment": {
                "id": 1,
                "marketplace_id": 1,
                "package_id": 1,
                "status": "created"
            }
        }

        responses.add(
            responses.POST,
            'https://tassi-api.exanora.com/shipments',
            json=mock_response,
            status=201
        )

        shipment = Shipment.create(payload)
        assert hasattr(shipment, 'id')
        assert shipment.status == "created"

    @responses.activate
    def test_create_validation_error(self):
        """Test de validation avec données invalides"""
        invalid_payload = {
            "marketplace_id": "1",
            "customer": {
                "first_name": "Judicaël"
                # Champs requis manquants
            }
        }

        responses.add(
            responses.POST,
            'https://tassi-api.exanora.com/shipments',
            json={"error": "Missing required customer fields"},
            status=400
        )

        with pytest.raises(ApiConnectionError):
            Shipment.create(invalid_payload)

    @responses.activate
    def test_create_invalid_package_weight(self):
        """Test avec poids de package invalide"""
        payload = {
            "marketplace_id": "1",
            "customer": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com"
            },
            "package": {
                "description": "Test package",
                "weight": -5,
                "dimensions": "invalid"
            }
        }

        responses.add(
            responses.POST,
            'https://tassi-api.exanora.com/shipments',
            json={"error": "Invalid package weight or dimensions"},
            status=400
        )

        with pytest.raises(ApiConnectionError):
            Shipment.create(payload)

    @responses.activate
    def test_create_with_pickup_point(self):
        """Test avec création d'un point de retrait"""
        payload = {
            "marketplace_id": "1",
            "customer": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "address": "Test Address",
                "city": "Cotonou",
                "country_code": "BJ"
            },
            "pickup_point": {
                "name": "Test Pickup",
                "address": "Test Address",
                "city": "Cotonou",
                "latitude": 6.3703,
                "longitude": 2.3912,
                "phone": "+22900000000"
            },
            "package": {
                "description": "Test",
                "weight": 5,
                "dimensions": "10x10x10"
            }
        }

        responses.add(
            responses.POST,
            'https://tassi-api.exanora.com/shipments',
            json={"shipment": {"id": 1}},
            status=201
        )

        shipment = Shipment.create(payload)
        assert hasattr(shipment, 'id')

    @responses.activate
    def test_create_with_route_stops(self):
        """Test avec des arrêts sur la route"""
        payload = {
            "marketplace_id": "1",
            "customer": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com"
            },
            "package": {
                "description": "Test package",
                "weight": 2.5
            },
            "route": {
                "origin": "Cotonou",
                "destination": "Porto-Novo",
                "stops": [
                    {
                        "city": "Sèmè-Kpodji",
                        "address": "Centre ville",
                        "latitude": 6.3512,
                        "longitude": 2.4987
                    },
                    {
                        "city": "Adjarra",
                        "address": "Marché central",
                        "latitude": 6.4123,
                        "longitude": 2.5234
                    }
                ]
            }
        }

        responses.add(
            responses.POST,
            'https://tassi-api.exanora.com/shipments',
            json={"shipment": {"id": 1, "route_stops_count": 2}},
            status=201
        )

        shipment = Shipment.create(payload)
        assert hasattr(shipment, 'id')
        assert shipment.route_stops_count == 2