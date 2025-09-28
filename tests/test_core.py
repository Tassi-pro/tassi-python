import pytest
import requests_mock
from tassi import Tassi
from tassi.exceptions import (
    TassiException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
)


class TestTassi:
    """Tests pour la classe principale Tassi."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.secret_key = "test_secret_key"
        self.tassi = Tassi(self.secret_key)

    def test_init_production(self):
        """Test d'initialisation en mode production."""
        tassi = Tassi("secret_key")
        assert tassi.base_url == Tassi.BASE_URL
        assert tassi.secret_key == "secret_key"
        assert not tassi.sandbox

    def test_init_sandbox(self):
        """Test d'initialisation en mode sandbox."""
        tassi = Tassi("secret_key", sandbox=True)
        assert tassi.base_url == Tassi.SANDBOX_URL
        assert tassi.sandbox

    def test_headers_setup(self):
        """Test de la configuration des headers."""
        tassi = Tassi("secret_key")
        headers = tassi.session.headers
        assert headers["Accept"] == "application/json"
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"] == "Bearer secret_key"

    def test_make_request_success(self):
        """Test d'une requête réussie."""
        expected_response = {"id": "123", "status": "success"}

        with requests_mock.Mocker() as m:
            m.post(f"{self.tassi.base_url}/test", json=expected_response)
            result = self.tassi._make_request("POST", "/test", data={"test": "data"})
            assert result == expected_response

    def test_make_request_authentication_error(self):
        """Test d'erreur d'authentification."""
        with requests_mock.Mocker() as m:
            m.post(f"{self.tassi.base_url}/test", status_code=401)

            with pytest.raises(AuthenticationError) as exc_info:
                self.tassi._make_request("POST", "/test")
            assert "Clé secrète invalide" in str(exc_info.value)

    def test_make_request_not_found_error(self):
        """Test d'erreur ressource non trouvée."""
        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/test", status_code=404)

            with pytest.raises(NotFoundError):
                self.tassi._make_request("GET", "/test")

    def test_make_request_validation_error(self):
        """Test d'erreur de validation."""
        with requests_mock.Mocker() as m:
            m.post(f"{self.tassi.base_url}/test", status_code=422, text="Validation failed")

            with pytest.raises(ValidationError) as exc_info:
                self.tassi._make_request("POST", "/test")
            assert "Erreur de validation" in str(exc_info.value)

    def test_create_shipment(self):
        """Test de création d'un shipment."""
        shipment_data = {
            "shipment": {
                "marketplace_id": "123",
                "customer": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                },
            }
        }
        expected_response = {"id": "ship_123", "status": "created"}

        with requests_mock.Mocker() as m:
            m.post(f"{self.tassi.base_url}/shipments", json=expected_response)
            result = self.tassi.create_shipment(shipment_data)
            assert result == expected_response

    def test_list_packages(self):
        """Test de récupération de la liste des packages."""
        expected_response = {"packages": [], "meta": {"total": 0}}

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/packages", json=expected_response)
            result = self.tassi.list_packages()
            assert result == expected_response

    def test_get_package(self):
        """Test de récupération d'un package."""
        package_id = "pkg_123"
        expected_response = {"id": package_id, "status": "in_transit"}

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/packages/{package_id}", json=expected_response)
            result = self.tassi.get_package(package_id)
            assert result == expected_response

    def test_update_package(self):
        """Test de mise à jour d'un package."""
        package_id = "pkg_123"
        update_data = {"status": "delivered"}
        expected_response = {"id": package_id, "status": "delivered"}

        with requests_mock.Mocker() as m:
            m.put(f"{self.tassi.base_url}/packages/{package_id}", json=expected_response)
            result = self.tassi.update_package(package_id, update_data)
            assert result == expected_response

    def test_track_package(self):
        """Test de suivi d'un package."""
        package_id = "pkg_123"
        expected_response = {"tracking_events": [], "current_status": "in_transit"}

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/packages/{package_id}/track", json=expected_response)
            result = self.tassi.track_package(package_id)
            assert result == expected_response

    def test_get_shipping_label(self):
        """Test de récupération d'une étiquette d'expédition."""
        package_id = "pkg_123"
        label_id = "lbl_456"
        expected_response = {"label_url": "https://example.com/label.pdf"}

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/packages/{package_id}/shipping_labels/{label_id}", json=expected_response)
            result = self.tassi.get_shipping_label(package_id, label_id)
            assert result == expected_response

    def test_get_carrier(self):
        """Test de récupération d'un transporteur."""
        carrier_id = "car_123"
        expected_response = {"id": carrier_id, "name": "DHL"}

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/carriers/{carrier_id}", json=expected_response)
            result = self.tassi.get_carrier(carrier_id)
            assert result == expected_response

    def test_get_carrier_with_include(self):
        """Test de récupération d'un transporteur avec paramètres."""
        carrier_id = "car_123"
        include = "services,pricing"
        expected_response = {"id": carrier_id, "services": []}

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/carriers/{carrier_id}?include={include}", json=expected_response)
            result = self.tassi.get_carrier(carrier_id, include=include)
            assert result == expected_response

    def test_update_carrier(self):
        """Test de mise à jour d'un transporteur."""
        carrier_id = "car_123"
        update_data = {"is_active": False}
        expected_response = {"id": carrier_id, "is_active": False}

        with requests_mock.Mocker() as m:
            m.put(f"{self.tassi.base_url}/carriers/{carrier_id}", json=expected_response)
            result = self.tassi.update_carrier(carrier_id, update_data)
            assert result == expected_response

    def test_get_marketplace(self):
        """Test de récupération d'une marketplace."""
        marketplace_id = "mkt_123"
        expected_response = {"id": marketplace_id, "name": "Test Market"}

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/marketplaces/{marketplace_id}", json=expected_response)
            result = self.tassi.get_marketplace(marketplace_id)
            assert result == expected_response

    def test_update_marketplace(self):
        """Test de mise à jour d'une marketplace."""
        marketplace_id = "mkt_123"
        update_data = {
            "name": "Market1",
            "api_name": "market1",
            "website": "market1.com",
            "email": "franckaigba4@gmail.com",
            "country_code": "BJ",
        }
        expected_response = update_data.copy()
        expected_response["id"] = marketplace_id

        with requests_mock.Mocker() as m:
            m.put(f"{self.tassi.base_url}/marketplaces/{marketplace_id}", json=expected_response)
            result = self.tassi.update_marketplace(marketplace_id, update_data)
            assert result == expected_response

    def test_get_marketplace_wallet_history(self):
        """Test de récupération de l'historique du portefeuille."""
        marketplace_id = "mkt_123"
        expected_response = {
            "wallet_movements": [],
            "meta": {
                "current_page": 1,
                "next_page": None,
                "prev_page": None,
                "per_page": 25,
                "total_pages": 0,
                "total_count": 0,
            },
        }

        with requests_mock.Mocker() as m:
            m.get(f"{self.tassi.base_url}/marketplaces/{marketplace_id}/wallet_history", json=expected_response)
            result = self.tassi.get_marketplace_wallet_history(marketplace_id)
            assert result == expected_response

    def test_timeout_configuration(self):
        """Test de configuration du timeout."""
        tassi = Tassi("secret_key", timeout=60)
        assert tassi.timeout == 60