# Tassi Python SDK

SDK Python officiel pour l'API Tassi - Solution complète de logistique et d'expédition.

## Installation

```bash
pip install tassi
```

## Configuration

```python
from tassi import Tassi

# Configuration de base
Tassi.set_api_key("votre_cle_api")
Tassi.set_environment("sandbox")  # ou "live"
```

## Utilisation

### Créer une expédition

```python
from tassi import Shipment

shipment_data = {
    "marketplace_id": "1",
    "customer": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "address": "123 Main Street",
        "city": "Cotonou",
        "country_code": "BJ"
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

try:
    shipment = Shipment.create(shipment_data)
    print(f"Expédition créée avec succès")
    print(f"ID: {shipment.id}")
    print(f"Status: {shipment.status}")
except Exception as e:
    print(f"Erreur: {e}")
```

### Gérer les packages

```python
from tassi import Package

# Lister tous les packages
result = Package.all()
print(f"Nombre de packages: {len(result.packages)}")

for pkg in result.packages:
    print(f"- {pkg.tracking_number}: {pkg.status}")

# Récupérer un package spécifique
package = Package.retrieve(4)
print(f"Package: {package.tracking_number}")
print(f"Status: {package.status}")
print(f"Description: {package.description}")

# Mettre à jour un package
updated_package = Package.update(4, {
    "description": "Nouvelle description",
    "weight": "15.0"
})
print(f"Package mis à jour: {updated_package.description}")

# Suivre un package
tracking_info = package.track()
print(f"Informations de suivi récupérées")

# Récupérer l'étiquette d'expédition
label = package.get_shipping_label(1)
print(f"Étiquette: {label.shipping_label.filename}")
```

### Gérer les marketplaces

```python
from tassi import Marketplace

# Récupérer une marketplace
marketplace = Marketplace.retrieve(1)
print(f"Marketplace: {marketplace.name}")
print(f"Active: {marketplace.is_active}")
print(f"Nombre de packages: {marketplace.packages_count}")

# Mettre à jour une marketplace
updated_marketplace = Marketplace.update(1, {
    "website": "nouveau-site.com"
})
print(f"Marketplace mise à jour")

# Récupérer l'historique du portefeuille
history = marketplace.get_wallet_history()
print(f"Nombre de mouvements: {len(history.wallet_movements)}")

for movement in history.wallet_movements:
    print(f"{movement.action}: {movement.amount} ({movement.created_at})")
```

## Structure de l'API

### Classes principales

- **Tassi** : Configuration globale (API key, environnement)
- **TassiObject** : Classe de base pour tous les objets
- **Resource** : Classe de base avec méthodes CRUD héritées
- **Requestor** : Gestionnaire des requêtes HTTP

### Ressources disponibles

#### 1. Package

**Méthodes de classe :**

- `Package.all(params=None, headers=None)` - Liste tous les packages
- `Package.retrieve(id, headers=None)` - Récupère un package par ID
- `Package.update(id, params, headers=None)` - Met à jour un package

**Méthodes d'instance :**

- `package.track(headers=None)` - Suivi du package
- `package.get_shipping_label(label_id, headers=None)` - Récupère l'étiquette d'expédition

#### 2. Shipment

**Méthodes de classe :**

- `Shipment.create(params, headers=None)` - Crée une nouvelle expédition

#### 3. Marketplace

**Méthodes de classe :**

- `Marketplace.retrieve(id, headers=None)` - Récupère une marketplace
- `Marketplace.update(id, params, headers=None)` - Met à jour une marketplace

**Méthodes d'instance :**

- `marketplace.get_wallet_history(params=None, headers=None)` - Historique du portefeuille

## Gestion des erreurs

```python
from tassi.error import (
    TassiError,
    InvalidRequestError,
    ApiConnectionError,
    AuthenticationError,
    NotFoundError,
    ValidationError
)

try:
    package = Package.retrieve("invalid_id")
except InvalidRequestError as e:
    print(f"Paramètres invalides: {e}")
except NotFoundError as e:
    print(f"Package non trouvé: {e}")
except ApiConnectionError as e:
    print(f"Erreur de connexion (HTTP {e.http_status}): {e}")
except AuthenticationError as e:
    print(f"Erreur d'authentification: {e}")
except TassiError as e:
    print(f"Erreur Tassi: {e}")
```

### Hiérarchie des exceptions

```
TassiError (base)
├── InvalidRequestError       # Paramètres invalides
├── ApiConnectionError        # Erreur HTTP
├── AuthenticationError       # Authentification échouée
├── NotFoundError            # Ressource non trouvée (404)
└── ValidationError          # Validation des données échouée
```

## Tests

### Tests unitaires (avec mocks)

```bash
# Installation des dépendances de développement
pip install -e .[dev]

# Lancer tous les tests
pytest
```

## Structure du projet

```
tassi-python/
├── tassi/
│   ├── __init__.py          # Point d'entrée, exports
│   ├── tassi.py             # Configuration principale
│   ├── error.py             # Exceptions personnalisées
│   ├── requestor.py         # Gestionnaire HTTP
│   ├── tassi_object.py      # Classe de base
│   ├── resource.py          # Ressource de base avec CRUD
│   ├── util.py              # Utilitaires
│   ├── package.py           # Ressource Package
│   ├── shipment.py          # Ressource Shipment
│   └── marketplace.py       # Ressource Marketplace
├── tests/
│   ├── test_package.py      # Tests Package
│   ├── test_shipment.py     # Tests Shipment
│   └── test_marketplace.py  # Tests Marketplace
├── setup.py                 # Configuration du package
├── requirements.txt         # Dépendances
└── README.md               # Documentation
```

## Dépendances

### Production

```
requests>=2.25.0       # Client HTTP
inflection>=0.5.0      # Pluralisation des noms de ressources
```

### Développement

```
pytest>=6.0.0          # Framework de tests
responses>=0.18.0      # Mocking des requêtes HTTP
pytest-cov>=2.10.0     # Couverture de code
```

## Exemples complets

### Workflow complet : Créer et suivre une expédition

```python
from tassi import Tassi, Shipment, Package

# Configuration
Tassi.set_api_key("votre_cle_api")

# Créer une expédition
shipment_data = {
    "marketplace_id": "1",
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
        "weight": 1.2,
        "dimensions": "30x20x15",
        "declared_value": "50",
        "currency": "XOF"
    },
    "route": {
        "origin": "Cotonou",
        "destination": "Abomey-Calavi"
    }
}

try:
    # Créer l'expédition
    shipment = Shipment.create(shipment_data)
    print(f"Expédition créée: {shipment.id}")

    # Récupérer les packages associés
    packages = Package.all({"shipment_id": shipment.id})

    if hasattr(packages, 'packages') and len(packages.packages) > 0:
        package = packages.packages[0]
        print(f"Package ID: {package.id}")
        print(f"Tracking: {package.tracking_number}")

        # Suivre le package
        tracking = package.track()
        print(f"Statut: suivi récupéré")

except Exception as e:
    print(f"Erreur: {e}")
```

### Gérer plusieurs marketplaces

```python
from tassi import Tassi, Marketplace

Tassi.set_api_key("votre_cle_api")

# Récupérer une marketplace
marketplace = Marketplace.retrieve(1)
print(f"Marketplace: {marketplace.name}")
print(f"Active: {marketplace.is_active}")

# Mettre à jour si nécessaire
if not marketplace.is_active:
    updated = Marketplace.update(1, {"is_active": True})
    print("Marketplace activée")

# Vérifier l'historique du portefeuille
history = marketplace.get_wallet_history()
total = len(history.wallet_movements) if hasattr(history, 'wallet_movements') else 0
print(f"Total des mouvements: {total}")

# Afficher les derniers mouvements
if hasattr(history, 'wallet_movements'):
    for movement in history.wallet_movements[:5]:
        print(f"- {movement.action}: {movement.amount}")
```

## Support et contribution

### Signaler un bug

Ouvrez une issue sur [GitHub Issues](https://github.com/Tassi-pro/tassi-python/issues)

### Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

### Guidelines de contribution

- Écrire des tests pour toute nouvelle fonctionnalité
- Suivre les conventions de code existantes
- Documenter les changements dans le README
- S'assurer que tous les tests passent (`pytest`)

## Informations supplémentaires

- **Version** : 1.0.0
- **Python** : >= 3.8
- **URL de l'API** : https://tassi-api.exanora.com
- **Environnements** : sandbox, live

---

**Tassi Python SDK** - Simplifiez vos intégrations logistiques
