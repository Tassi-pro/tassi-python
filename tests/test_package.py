"""Tests pour la ressource Package"""
import pytest
import responses
from tassi import Tassi, Package
from tassi.error import InvalidRequestError


class TestPackage:
    """Tests pour Package"""

    def setup_method(self):
        """Configuration avant chaque test"""
        Tassi.set_api_key('test_api_key')
        Tassi.set_environment('sandbox')

    @responses.activate
    def test_all(self):
        """Test de la liste des packages"""
        mock_response = {
            "packages": [
                {
                    "id": 4,
                    "tracking_number": "tassi_TRK_CFE667F2DB8E9578",
                    "status": "in_transit",
                    "description": "Colis test contenant accessoires électroniques",
                    "weight": "5.0",
                    "dimensions": "10x10x10",
                    "declared_value": "100.0",
                    "currency": "USD",
                    "insurance": False,
                    "signature_required": True
                }
            ],
            "meta": {
                "current_page": 1,
                "total_count": 4
            }
        }

        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/packages',
            json=mock_response,
            status=200
        )

        result = Package.all()
        assert hasattr(result, 'packages')
        assert isinstance(result.packages, list)
        assert len(result.packages) > 0
        assert result.packages[0].tracking_number == "tassi_TRK_CFE667F2DB8E9578"
        assert result.packages[0].status == "in_transit"
        assert result.packages[0].insurance is False
        assert result.packages[0].signature_required is True

    @responses.activate
    def test_all_with_pagination(self):
        """Test de la liste avec pagination"""
        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/packages',
            json={"packages": [], "meta": {}},
            status=200
        )

        Package.all({"page": 2, "per_page": 10})

    @responses.activate
    def test_retrieve(self):
        """Test de récupération d'un package"""
        mock_response = {
            "package": {
                "id": 4,
                "tracking_number": "tassi_TRK_CFE667F2DB8E9578",
                "status": "in_transit",
                "description": "Colis test contenant accessoires électroniques",
                "weight": "5.0",
                "dimensions": "10x10x10",
                "declared_value": "100.0",
                "currency": "USD",
                "insurance": False,
                "signature_required": True
            }
        }

        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/packages/4',
            json=mock_response,
            status=200
        )

        pkg = Package.retrieve(4)
        assert pkg.id == 4
        assert pkg.tracking_number == "tassi_TRK_CFE667F2DB8E9578"
        assert pkg.status == "in_transit"
        assert pkg.weight == "5.0"
        assert pkg.insurance is False
        assert pkg.signature_required is True

    def test_retrieve_invalid_id(self):
        """Test avec un ID invalide"""
        with pytest.raises(InvalidRequestError):
            Package.retrieve(None)

    @responses.activate
    def test_update(self):
        """Test de mise à jour d'un package"""
        mock_response = {
            "package": {
                "id": 4,
                "tracking_number": "tassi_TRK_CFE667F2DB8E9578",
                "status": "in_transit",
                "description": "Colis test contenant accessoires de coifure",
                "weight": "15.0",
                "dimensions": "10x10x10",
                "declared_value": "100.0",
                "currency": "USD"
            }
        }

        responses.add(
            responses.PUT,
            'https://tassi-api.exanora.com/packages/4',
            json=mock_response,
            status=200
        )

        pkg = Package.update(4, {
            "description": "Colis test contenant accessoires de coifure",
            "weight": "15.0"
        })

        assert pkg.description == "Colis test contenant accessoires de coifure"
        assert pkg.weight == "15.0"

    @responses.activate
    def test_track(self):
        """Test de suivi d'un package"""
        mock_response = {}

        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/packages/4/track',
            json=mock_response,
            status=200
        )

        pkg = Package()
        pkg.id = 4
        result = pkg.track()
        assert result is not None

    @responses.activate
    def test_get_shipping_label(self):
        """Test de récupération d'étiquette"""
        mock_response = {
            "shipping_label": {
                "id": 1,
                "label_type": "shipping_label",
                "format": "pdf",
                "size": "a4",
                "file_url": None,
                "checksum": "f36a40debd30d81fdabf9285bcf5b573c828c21a0b839f7c85be62bdf7f2a9d1",
                "version": 1,
                "package_id": 1,
                "filename": "tassi_TRK_99F75AD8447EA4C0_v1.pdf"
            }
        }

        responses.add(
            responses.GET,
            'https://tassi-api.exanora.com/packages/1/shipping_labels/1',
            json=mock_response,
            status=200
        )

        pkg = Package()
        pkg.id = 1
        result = pkg.get_shipping_label(1)

        assert hasattr(result, 'shipping_label')
        assert result.shipping_label.label_type == "shipping_label"
        assert result.shipping_label.format == "pdf"
        assert result.shipping_label.version == 1
        assert result.shipping_label.filename == "tassi_TRK_99F75AD8447EA4C0_v1.pdf"