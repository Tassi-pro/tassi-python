"""Tests pour la ressource Marketplace"""
import pytest
import responses
from tassi import Tassi, Marketplace
from tassi.error import ApiConnectionError


class TestMarketplace:
    """Tests pour Marketplace"""

    def setup_method(self):
        """Configuration avant chaque test"""
        Tassi.set_api_key('test_api_key')
        Tassi.set_environment('sandbox')

    @responses.activate
    def test_retrieve(self):
        """Test de récupération d'une marketplace"""
        mock_response = {
            "id": 1,
            "name": "Market1",
            "api_name": "market1",
            "website": "market1.com",
            "is_active": True,
            "api_configuration": {},
            "country_code": "BJ",
            "phone_number": "0163085267",
            "email": "franckaigba4@gmail.com",
            "customers_count": 0,
            "packages_count": 4
        }

        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/marketplaces/1',
            json=mock_response,
            status=200
        )

        marketplace = Marketplace.retrieve(1)
        assert marketplace.id == 1
        assert marketplace.name == "Market1"
        assert marketplace.api_name == "market1"
        assert marketplace.is_active is True
        assert marketplace.country_code == "BJ"
        assert marketplace.packages_count == 4

    @responses.activate
    def test_update(self):
        """Test de mise à jour d'une marketplace"""
        mock_response = {
            "id": 1,
            "name": "Market1",
            "api_name": "market1",
            "website": "market-app.com",
            "is_active": True,
            "api_configuration": {},
            "country_code": "BJ",
            "phone_number": "0163085267",
            "email": "franckaigba4@gmail.com",
            "customers_count": 0,
            "packages_count": 4
        }

        responses.add(
            responses.PUT,
            'https://tassi-api.exanora.com/marketplaces/1',
            json=mock_response,
            status=200
        )

        marketplace = Marketplace.update(1, {"website": "market-app.com"})
        assert marketplace.website == "market-app.com"

    @responses.activate
    def test_update_validation_error(self):
        """Test de validation avec email invalide"""
        responses.add(
            responses.PUT,
            'https://tassi-api.exanora.com/marketplaces/1',
            json={"error": "Invalid email format"},
            status=400
        )

        with pytest.raises(ApiConnectionError):
            Marketplace.update(1, {"email": "invalid-email"})

    @responses.activate
    def test_get_wallet_history(self):
        """Test de récupération de l'historique du wallet"""
        mock_response = {
            "wallet_movements": [
                {
                    "id": 7,
                    "action": "Credit",
                    "description": "Test credit",
                    "amount": "1.0",
                    "created_at": "2025-09-27T12:43:59Z",
                    "wallet_id": 1
                },
                {
                    "id": 6,
                    "action": "Credit",
                    "description": "Test credit",
                    "amount": "1.0",
                    "created_at": "2025-09-27T12:43:57Z",
                    "wallet_id": 1
                },
                {
                    "id": 5,
                    "action": "Debit",
                    "description": "Test debit",
                    "amount": "1.0",
                    "created_at": "2025-09-27T12:43:46Z",
                    "wallet_id": 1
                }
            ]
        }

        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/marketplaces/1/wallet_history',
            json=mock_response,
            status=200
        )

        marketplace = Marketplace()
        marketplace.id = 1
        result = marketplace.get_wallet_history()

        assert hasattr(result, 'wallet_movements')
        assert isinstance(result.wallet_movements, list)
        assert len(result.wallet_movements) == 3
        assert result.wallet_movements[0].action == "Credit"
        assert result.wallet_movements[2].action == "Debit"

    @responses.activate
    def test_get_wallet_history_with_pagination(self):
        """Test de l'historique avec pagination"""
        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/marketplaces/1/wallet_history',
            json={"wallet_movements": []},
            status=200
        )

        marketplace = Marketplace()
        marketplace.id = 1
        marketplace.get_wallet_history({"page": 2, "limit": 10})

    @responses.activate
    def test_get_wallet_history_empty(self):
        """Test avec historique vide"""
        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/marketplaces/1/wallet_history',
            json={"wallet_movements": []},
            status=200
        )

        marketplace = Marketplace()
        marketplace.id = 1
        result = marketplace.get_wallet_history()

        assert hasattr(result, 'wallet_movements')
        assert isinstance(result.wallet_movements, list)
        assert len(result.wallet_movements) == 0

    @responses.activate
    def test_save(self):
        """Test de sauvegarde des modifications"""
        mock_response = {
            "id": 1,
            "name": "Updated Market",
            "website": "updated.com"
        }

        responses.add(
            responses.PUT,
            'https://tassi-api.exanora.com/marketplaces/1',
            json=mock_response,
            status=200
        )

        marketplace = Marketplace()
        marketplace.id = 1
        marketplace.name = "Updated Market"
        marketplace.website = "updated.com"

        saved = marketplace.save()
        assert saved.name == "Updated Market"
        assert saved.website == "updated.com"

    @responses.activate
    def test_marketplace_status_management(self):
        """Test de gestion du statut de la marketplace"""
        # Test désactivation
        responses.add(
            responses.PUT,
            'https://tassi-api.exanora.com/marketplaces/1',
            json={"id": 1, "is_active": False},
            status=200
        )

        marketplace = Marketplace.update(1, {"is_active": False})
        assert marketplace.is_active is False

        # Test réactivation
        responses.add(
            responses.PUT,
            'https://tassi-api.exanora.com/marketplaces/1',
            json={"id": 1, "is_active": True},
            status=200
        )

        marketplace = Marketplace.update(1, {"is_active": True})
        assert marketplace.is_active is True