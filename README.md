# Tassi Python SDK

SDK Python officiel pour l'API Tassi - Solution complète de logistique et d'expédition.

## 📋 Table des matières

- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [API Reference](#api-reference)
- [Exemples](#exemples)
- [Tests](#tests)
- [Contribution](#contribution)
- [Licence](#licence)

## 🚀 Installation

```bash
pip install tassi
```

## ⚙️ Configuration

```python
from tassi import Tassi

# Initialisation en mode production
tassi = Tassi(secret_key="votre_cle_secrete")

# Initialisation en mode sandbox (futur)
tassi = Tassi(secret_key="votre_cle_secrete", sandbox=True)
```

## 🎯 Utilisation

### Créer un shipment

```python
from tassi import Tassi

tassi = Tassi("votre_cle_secrete")

shipment_data = {
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

try:
    shipment = tassi.create_shipment(shipment_data)
    print(f"Shipment créé: {shipment['id']}")
except Exception as e:
    print(f"Erreur: {e}")
```

### Suivre un package

```python
try:
    tracking_info = tassi.track_package("package_id")
    print(f"Statut: {tracking_info['current_status']}")
    print(f"Événements: {tracking_info['tracking_events']}")
except Exception as e:
    print(f"Erreur: {e}")
```

### Gérer les packages

```python
# Lister tous les packages
packages = tassi.list_packages()

# Récupérer un package spécifique
package = tassi.get_package("package_id")

# Mettre à jour un package
updated_package = tassi.update_package("package_id", {
    "status": "delivered"
})
```

### Gérer les marketplaces

```python
# Récupérer une marketplace
marketplace = tassi.get_marketplace("marketplace_id")

# Mettre à jour une marketplace
updated_marketplace = tassi.update_marketplace("marketplace_id", {
    "name": "Nouveau nom",
    "is_active": True
})

# Historique du portefeuille
wallet_history = tassi.get_marketplace_wallet_history("marketplace_id")
```

## 📚 API Reference

### Classe principale

#### `Tassi(secret_key, sandbox=False, timeout=30)`

- `secret_key` (str): Clé secrète d'authentification
- `sandbox` (bool): Mode sandbox (défaut: False)
- `timeout` (int): Timeout des requêtes en secondes (défaut: 30)

### Méthodes disponibles

#### Shipments
- `create_shipment(shipment_data)` - Créer un nouveau shipment

#### Packages
- `list_packages(params=None)` - Lister les packages
- `get_package(package_id)` - Récupérer un package
- `update_package(package_id, data)` - Mettre à jour un package
- `track_package(package_id)` - Suivre un package
- `get_shipping_label(package_id, label_id)` - Récupérer une étiquette

#### Carriers
- `get_carrier(carrier_id, include=None)` - Récupérer un transporteur
- `update_carrier(carrier_id, data)` - Mettre à jour un transporteur

#### Marketplaces
- `get_marketplace(marketplace_id)` - Récupérer une marketplace
- `update_marketplace(marketplace_id, data)` - Mettre à jour une marketplace
- `get_marketplace_wallet_history(marketplace_id, params=None)` - Historique du portefeuille

## 🔧 Gestion des erreurs

Le SDK utilise des exceptions personnalisées :

```python
from tassi.exceptions import (
    TassiException,
    AuthenticationError,
    ValidationError,
    NotFoundError
)

try:
    result = tassi.get_package("invalid_id")
except AuthenticationError:
    print("Clé secrète invalide")
except NotFoundError:
    print("Package non trouvé")
except ValidationError:
    print("Données invalides")
except TassiException as e:
    print(f"Erreur Tassi: {e}")
```

## 🎨 Exemples complets

### Workflow complet de shipment

```python
from tassi import Tassi
from tassi.exceptions import TassiException

def create_and_track_shipment():
    tassi = Tassi("votre_cle_secrete")

    # 1. Créer le shipment
    shipment_data = {
        "shipment": {
            "marketplace_id": "mkt_123",
            "customer": {
                "first_name": "Marie",
                "last_name": "Dupont",
                "email": "marie@example.com",
                "address": "456 Rue de la Paix",
                "city": "Cotonou",
                "country_code": "BJ"
            },
            "package": {
                "description": "Vêtements",
                "weight": "1.2",
                "dimensions": "30x20x15",
                "declared_value": "50",
                "currency": "XOF",
                "insurance": True
            },
            "route": {
                "origin": "Cotonou",
                "destination": "Abomey-Calavi",
                "stops": []
            }
        }
    }

    try:
        # Créer le shipment
        shipment = tassi.create_shipment(shipment_data)
        print(f"✅ Shipment créé: {shipment.get('id')}")

        # Récupérer les packages associés
        packages = tassi.list_packages({"shipment_id": shipment.get('id')})

        if packages.get('packages'):
            package_id = packages['packages'][0]['id']

            # Suivre le package
            tracking = tassi.track_package(package_id)
            print(f"📦 Statut du package: {tracking.get('current_status')}")

        return shipment

    except TassiException as e:
        print(f"❌ Erreur: {e}")
        return None

# Utilisation
shipment = create_and_track_shipment()
```

### Gestion des marketplaces

```python
def manage_marketplace(marketplace_id):
    tassi = Tassi("votre_cle_secrete")

    try:
        # Récupérer les détails
        marketplace = tassi.get_marketplace(marketplace_id)
        print(f"Marketplace: {marketplace.get('name')}")

        # Mettre à jour si nécessaire
        if not marketplace.get('is_active'):
            updated = tassi.update_marketplace(marketplace_id, {
                "is_active": True
            })
            print("✅ Marketplace activée")

        # Vérifier l'historique du portefeuille
        wallet_history = tassi.get_marketplace_wallet_history(marketplace_id)
        total_movements = wallet_history.get('meta', {}).get('total_count', 0)
        print(f"💰 Total des mouvements: {total_movements}")

    except TassiException as e:
        print(f"❌ Erreur: {e}")

# Utilisation
manage_marketplace("mkt_123")
```

## 🔧 Développement

### Installation pour le développement

```bash
git clone https://github.com/Tassi-pro/tassi-python.git
cd tassi-python
pip install -e .[dev]
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

### Guidelines

- Écrivez des tests pour toute nouvelle fonctionnalité
- Respectez les conventions de codage existantes
- Documentez vos changements dans le README si nécessaire
- Assurez-vous que tous les tests passent

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

- **Documentation**: [docs.tassi.com](https://docs.tassi.com)
- **Issues**: [GitHub Issues](https://github.com/Tassi-pro/tassi-python/issues)
- **Email**: dev@tassi.com

---

**Tassi Python SDK** - Simplifiez vos intégrations logistiques 🚀