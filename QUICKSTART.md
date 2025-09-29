# Guide de démarrage rapide - Tassi Python SDK

Ce guide vous accompagne pas à pas pour installer et utiliser le SDK Tassi.

## Étape 1 : Créer votre projet

```bash
# Créer un nouveau dossier pour votre projet
mkdir mon-projet-tassi
cd mon-projet-tassi
```

## Étape 2 : Configurer l'environnement virtuel

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows
```

Vous devriez voir `(venv)` au début de votre ligne de commande.

## Étape 3 : Installer Tassi

```bash
# Installer depuis GitHub
pip install git+https://github.com/Tassi-pro/tassi-python.git
```

**Sortie attendue :**
```
Collecting git+https://github.com/Tassi-pro/tassi-python.git
  Cloning https://github.com/Tassi-pro/tassi-python.git to /tmp/...
Successfully installed tassi-1.0.0 requests-2.31.0 inflection-0.5.1
```

## Étape 4 : Vérifier l'installation

```bash
python -c "from tassi import Tassi; print('Version:', Tassi.VERSION)"
```

**Sortie attendue :**
```
Version: 1.0.0
```

## Étape 5 : Créer votre premier script

Créez un fichier `test_tassi.py` :

```python
from tassi import Tassi, Package

# Configuration
Tassi.set_api_key("votre_cle_api_ici")
Tassi.set_environment("sandbox")

# Test de connexion
try:
    # Récupérer la liste des packages
    result = Package.all()

    print("Connexion réussie à l'API Tassi!")
    print(f"SDK Version: {Tassi.VERSION}")
    print(f"Environnement: {Tassi.get_environment()}")

    if hasattr(result, 'packages'):
        print(f"Nombre de packages: {len(result.packages)}")
    else:
        print("Aucun package trouvé")

except Exception as e:
    print(f"Erreur de connexion: {e}")
```

## Étape 6 : Configurer vos credentials

### Option A : Directement dans le code (pour tester)

```python
Tassi.set_api_key("sk_test_votre_cle_ici")
```

### Option B : Variables d'environnement (recommandé)

**1. Installer python-dotenv :**
```bash
pip install python-dotenv
```

**2. Créer un fichier `.env` :**
```bash
TASSI_API_KEY=sk_test_votre_cle_ici
TASSI_ENVIRONMENT=sandbox
```

**3. Ajouter `.env` au `.gitignore` :**
```bash
echo ".env" >> .gitignore
```

**4. Utiliser dans votre code :**
```python
import os
from dotenv import load_dotenv
from tassi import Tassi

load_dotenv()

Tassi.set_api_key(os.getenv('TASSI_API_KEY'))
Tassi.set_environment(os.getenv('TASSI_ENVIRONMENT'))
```

## Étape 7 : Exécuter votre script

```bash
python test_tassi.py
```

**Sortie attendue :**
```
Connexion réussie à l'API Tassi!
SDK Version: 1.0.0
Environnement: sandbox
Nombre de packages: 5
```

## Exemples d'utilisation

### Exemple 1 : Lister les packages

```python
from tassi import Tassi, Package

Tassi.set_api_key("votre_cle")

# Récupérer tous les packages
result = Package.all()

for pkg in result.packages:
    print(f"Package {pkg.id}:")
    print(f"  - Tracking: {pkg.tracking_number}")
    print(f"  - Status: {pkg.status}")
    print(f"  - Description: {pkg.description}")
    print()
```

### Exemple 2 : Créer une expédition

```python
from tassi import Tassi, Shipment

Tassi.set_api_key("votre_cle")

shipment_data = {
    "marketplace_id": "1",
    "customer": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "address": "123 Main St",
        "city": "Cotonou",
        "country_code": "BJ"
    },
    "package": {
        "description": "Test package",
        "weight": 2.5,
        "dimensions": "20x15x10",
        "declared_value": "50",
        "currency": "XOF"
    },
    "route": {
        "origin": "Cotonou",
        "destination": "Porto-Novo"
    }
}

shipment = Shipment.create(shipment_data)
print(f"Expédition créée: {shipment.id}")
print(f"Status: {shipment.status}")
```

### Exemple 3 : Suivre un package

```python
from tassi import Tassi, Package

Tassi.set_api_key("votre_cle")

# Récupérer un package
package = Package.retrieve(4)

# Suivre le package
tracking = package.track()
print("Informations de suivi récupérées")
```

### Exemple 4 : Gérer une marketplace

```python
from tassi import Tassi, Marketplace

Tassi.set_api_key("votre_cle")

# Récupérer une marketplace
marketplace = Marketplace.retrieve(1)
print(f"Marketplace: {marketplace.name}")
print(f"Active: {marketplace.is_active}")

# Historique du wallet
history = marketplace.get_wallet_history()
print(f"Mouvements: {len(history.wallet_movements)}")
```

## Structure recommandée du projet

```
mon-projet-tassi/
├── venv/                    # Environnement virtuel
├── .env                     # Variables d'environnement (ne pas committer)
├── .gitignore              # Fichiers à ignorer
├── requirements.txt         # Dépendances
├── config.py               # Configuration centralisée
└── app.py                  # Votre application
```

### requirements.txt

```txt
git+https://github.com/Tassi-pro/tassi-python.git
python-dotenv>=1.0.0
```

### .gitignore

```txt
venv/
.env
__pycache__/
*.pyc
.pytest_cache/
```

### config.py

```python
import os
from dotenv import load_dotenv
from tassi import Tassi

load_dotenv()

# Configuration Tassi
Tassi.set_api_key(os.getenv('TASSI_API_KEY'))
Tassi.set_environment(os.getenv('TASSI_ENVIRONMENT', 'sandbox'))

# Autres configurations...
```

### app.py

```python
import config  # Charge automatiquement la configuration
from tassi import Package, Shipment, Marketplace

# Votre code ici
packages = Package.all()
print(f"Packages: {len(packages.packages)}")
```

## Gestion des erreurs

```python
from tassi import Tassi, Package
from tassi.error import (
    TassiError,
    InvalidRequestError,
    ApiConnectionError,
    NotFoundError
)

Tassi.set_api_key("votre_cle")

try:
    package = Package.retrieve(999999)
except NotFoundError:
    print("Package non trouvé")
except ApiConnectionError as e:
    print(f"Erreur de connexion: HTTP {e.http_status}")
except InvalidRequestError as e:
    print(f"Paramètres invalides: {e}")
except TassiError as e:
    print(f"Erreur Tassi: {e}")
```

## Prochaines étapes

1. **Lire la documentation complète** : [README.md](README.md)
2. **Explorer les tests** : Voir les fichiers dans `tests/`
4. **Rejoindre la communauté** : [GitHub Issues](https://github.com/Tassi-pro/tassi-python/issues)

## Commandes utiles

```bash
# Activer l'environnement
source venv/bin/activate

# Installer/Mettre à jour Tassi
pip install --upgrade git+https://github.com/Tassi-pro/tassi-python.git

# Lancer les tests
pytest

# Désactiver l'environnement
deactivate
```

## Besoin d'aide ?

- **Documentation** : [README.md](README.md)
- **Issues** : [GitHub Issues](https://github.com/Tassi-pro/tassi-python/issues)

---

Vous êtes maintenant prêt à utiliser le SDK Tassi ! 🚀