# Tassi Python SDK

SDK Python officiel pour l'API Tassi - Solution complète de logistique et d'expédition.

## 🚀 Installation

```bash
pip install tassi
```

## ⚙️ Configuration

```python
from tassi import Tassi

# Configuration de base
Tassi.set_api_key("votre_cle_api")
Tassi.set_environment("sandbox")  # ou "production"
```

## 🎯 Utilisation

### Créer une expédition

```python
from tassi import Shipment

shipment_data = {
    "marketplace_id": "1",
    "customer": {
        "first_name": "Judicaël",
        "last_name": "DAKIN",
        "email": "customer@example.com",
        "address": "Rue 123, Houéyiho, Cotonou",
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
    print(f"Expédition créée: {shipment.id}")
except Exception as e:
    print(f"Erreur: {e}")
```

### Gérer les packages

```python
from tassi import Package

# Lister tous les packages
packages = Package.all()
print(f"Nombre de packages: {len(packages.packages)}")

# Récupérer un package spécifique
package = Package.retrieve(4)
print(f"Package: {package.tracking_number}")

# Mettre à jour un package
updated_package = Package.update(4, {
    "description": "Nouvelle description",
    "weight": "15.0"
})

# Suivre un package
tracking_info = package.track()

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

# Mettre à jour une marketplace
updated_marketplace = Marketplace.update(1, {
    "website": "nouveau-site.com"
})

# Historique du portefeuille
wallet_history = marketplace.get_wallet_history()
for movement in wallet_history.wallet_movements:
    print(f"{movement.action}: {movement.amount}")
```

## 📚 Structure de l'API

### Classes principales

- **Tassi** : Configuration globale (API key, environnement, version)
- **TassiObject** : Classe de base pour tous les objets
- **Resource** : Classe de base avec méthodes CRUD héritées
- **Requestor** : Gestionnaire des requêtes HTTP

### Ressources disponibles

1. **Package** :
   - `all()` - Liste des packages
   - `retrieve(id)` - Récupérer un package
   - `update(id, params)` - Mettre à jour
   - `track()` - Suivi du package
   - `get_shipping_label(label_id)` - Étiquette d'expédition

2. **Shipment** :
   - `create(params)` - Créer une expédition

3. **Marketplace** :
   - `retrieve(id)` - Récupérer une marketplace
   - `update(id, params)` - Mettre à jour
   - `get_wallet_history()` - Historique du wallet

## 🔧 Gestion des erreurs

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
except InvalidRequestError:
    print("ID invalide")
except NotFoundError:
    print("Package non trouvé")
except ApiConnectionError as e:
    print(f"Erreur de connexion: {e.http_status}")
except TassiError as e:
    print(f"Erreur Tassi: {e}")
```

## 🧪 Tests

Exécuter les tests :

```bash
# Installation des dépendances de développement
pip install -e .[dev]

# Lancer les tests
pytest

# Tests avec couverture
pytest --cov=tassi
```

## 🔧 Développement

### Structure du projet

```
tassi/
├── tassi/
│   ├── __init__.py          # Point d'entrée
│   ├── tassi.py             # Configuration principale
│   ├── error.py             # Exceptions
│   ├── requestor.py         # Gestionnaire HTTP
│   ├── tassi_object.py      # Classe de base
│   ├── resource.py          # Ressource de base
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

### Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

- **Documentation** : [docs.tassi.com](https://docs.tassi.com)
- **Issues** : [GitHub Issues](https://github.com/Tassi-pro/tassi-python/issues)
- **Email** : dev@tassi.com

---

**Tassi Python SDK** - Simplifiez vos intégrations logistiques 🚀