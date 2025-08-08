# Organisation des fichiers CSS - E-Menu Togo

## Structure des fichiers CSS

### 📁 `static/css/`

#### 1. `base.css` - Styles de base
- **Utilisation** : Tous les gabarits
- **Contenu** :
  - Variables CSS (couleurs, espacements)
  - Reset et styles de base
  - Navigation principale
  - Footer
  - Utilitaires communs
  - Responsive de base

#### 2. `auth.css` - Pages d'authentification
- **Utilisation** : `accounts/templates/base_auth.html`
- **Pages concernées** :
  - Connexion (`accounts/login.html`)
  - Inscription (`accounts/register_user.html`)
  - Changement de mot de passe
  - Suppression de compte
- **Contenu** :
  - Styles des formulaires d'authentification
  - Cartes d'authentification
  - Messages d'erreur/succès
  - Boutons d'authentification

#### 3. `dashboard.css` - Tableau de bord
- **Utilisation** : `accounts/templates/accounts/dashboard.html`
- **Contenu** :
  - Cartes de statistiques
  - Actions rapides
  - Activités récentes
  - Grille de navigation

#### 4. `structures.css` - Pages des structures
- **Utilisation** : Templates de l'app `structures`
- **Pages concernées** :
  - Liste des structures
  - Détail d'une structure
  - Formulaire d'enregistrement
- **Contenu** :
  - Section héro
  - Cartes des structures
  - Détail des structures
  - Formulaires de structure

#### 5. `plats.css` - Pages des plats
- **Utilisation** : Templates de l'app `plats`
- **Pages concernées** :
  - Liste des plats
  - Formulaire de plat
  - Modal de détail
- **Contenu** :
  - Cartes des plats
  - Modals de détail
  - Formulaires de plat
  - Filtres et recherche

#### 6. `menus.css` - Pages des menus
- **Utilisation** : Templates de l'app `menus`
- **Pages concernées** :
  - Liste des menus
  - Détail d'un menu
  - Formulaire de menu
- **Contenu** :
  - Cartes des menus
  - Détail des menus
  - Sélection des plats
  - Formulaires de menu

## Comment utiliser les CSS dans vos templates

### 1. Template de base (base.html)
```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <!-- CSS de base (toujours chargé) -->
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
    <!-- CSS spécifique au gabarit -->
    {% block extra_css %}{% endblock %}
</head>
```

### 2. Template d'authentification (base_auth.html)
```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <!-- CSS d'authentification -->
    <link rel="stylesheet" href="{% static 'css/auth.css' %}">
</head>
```

### 3. Template spécifique (ex: dashboard.html)
```html
{% extends 'base.html' %}
{% load static %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/dashboard.css' %}">
{% endblock %}
```

### 4. Template de structure
```html
{% extends 'base.html' %}
{% load static %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/structures.css' %}">
{% endblock %}
```

## Variables CSS disponibles

Toutes les couleurs et espacements sont définis dans `base.css` :

```css
:root {
    --bs-jaune: #FFD700;
    --bs-vert: #006B3F;
    --bs-rouge: #DC3545;
    --bs-gris: #6C757D;
    --bs-blanc: #FFFFFF;
    --bs-noir: #000000;
    --bs-gris-clair: #F8F9FA;
    --bs-gris-fonce: #343A40;
}
```

## Bonnes pratiques

1. **Toujours utiliser les variables CSS** pour les couleurs et espacements
2. **Charger le CSS de base** dans tous les templates
3. **Charger le CSS spécifique** dans le bloc `extra_css`
4. **Respecter la hiérarchie** : base.css → CSS spécifique
5. **Tester la responsivité** sur mobile et tablette

## Ajout d'un nouveau CSS

Pour ajouter un CSS pour une nouvelle application :

1. Créer le fichier `static/css/nouvelle_app.css`
2. Ajouter le lien dans le template :
```html
{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/nouvelle_app.css' %}">
{% endblock %}
```

## Maintenance

- **Modifications globales** : Éditer `base.css`
- **Modifications spécifiques** : Éditer le CSS correspondant
- **Nouvelles fonctionnalités** : Créer un nouveau fichier CSS
- **Optimisation** : Utiliser les variables CSS pour la cohérence
