# E-Menu Togo - Guide Rapide

## 🚀 Démarrage Rapide

### 1. Installation
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration Base de Données
```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 3. Créer un Superutilisateur
```bash
python manage.py createsuperuser
```

### 4. Démarrer le Serveur
```bash
python manage.py runserver
```

### 5. Accéder à l'Application
- **Interface principale** : http://127.0.0.1:8000/
- **Administration** : http://127.0.0.1:8000/admin/

## 📁 Fichiers Utiles

- `GUIDE_DEBUTANT.txt` - Guide complet pour débutants
- `COMMANDES_PROJET.bat` - Menu interactif Windows
- `COMMANDES_PROJET.sh` - Menu interactif Linux/macOS

## 🔧 Commandes Utiles

```bash
# Vérifier le projet
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic

# Ouvrir le shell Django
python manage.py shell

# Voir l'état des migrations
python manage.py showmigrations
```

## 📖 Documentation Complète

Consultez `GUIDE_DEBUTANT.txt` pour un guide détaillé avec :
- Configuration des bases de données (SQLite, PostgreSQL, MySQL)
- Structure du projet
- Fonctionnalités principales
- Dépannage
- Ressources utiles

## 🆘 Support

En cas de problème, consultez la section "DÉPANNAGE" dans `GUIDE_DEBUTANT.txt`

