#!/bin/bash

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e "    E-MENU TOGO - COMMANDES PROJET"
echo -e "========================================${NC}"
echo

# Fonction pour afficher le menu
show_menu() {
    echo -e "${YELLOW}Choisissez une option :${NC}"
    echo
    echo "1.  Activer l'environnement virtuel"
    echo "2.  Installer les dépendances"
    echo "3.  Créer les migrations"
    echo "4.  Appliquer les migrations"
    echo "5.  Créer un superutilisateur"
    echo "6.  Démarrer le serveur"
    echo "7.  Démarrer le serveur (port 8080)"
    echo "8.  Collecter les fichiers statiques"
    echo "9.  Vérifier le projet"
    echo "10. Ouvrir le shell Django"
    echo "11. Afficher les migrations"
    echo "12. Reset complet (attention!)"
    echo "13. Quitter"
    echo
}

# Fonction pour activer l'environnement virtuel
activate_env() {
    echo -e "${BLUE}Activation de l'environnement virtuel...${NC}"
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo -e "${GREEN}Environnement virtuel activé !${NC}"
    else
        echo -e "${YELLOW}Environnement virtuel non trouvé. Création...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        echo -e "${GREEN}Environnement virtuel créé et activé !${NC}"
    fi
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour installer les dépendances
install_deps() {
    echo -e "${BLUE}Installation des dépendances...${NC}"
    pip install -r requirements.txt
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour créer les migrations
make_migrations() {
    echo -e "${BLUE}Création des migrations...${NC}"
    python manage.py makemigrations
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour appliquer les migrations
migrate() {
    echo -e "${BLUE}Application des migrations...${NC}"
    python manage.py migrate
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour créer un superutilisateur
createsuperuser() {
    echo -e "${BLUE}Création d'un superutilisateur...${NC}"
    python manage.py createsuperuser
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour démarrer le serveur
runserver() {
    echo -e "${BLUE}Démarrage du serveur sur http://127.0.0.1:8000/${NC}"
    echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter le serveur${NC}"
    echo
    python manage.py runserver
}

# Fonction pour démarrer le serveur sur le port 8080
runserver_8080() {
    echo -e "${BLUE}Démarrage du serveur sur http://127.0.0.1:8080/${NC}"
    echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter le serveur${NC}"
    echo
    python manage.py runserver 8080
}

# Fonction pour collecter les fichiers statiques
collectstatic() {
    echo -e "${BLUE}Collecte des fichiers statiques...${NC}"
    python manage.py collectstatic --noinput
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour vérifier le projet
check() {
    echo -e "${BLUE}Vérification du projet...${NC}"
    python manage.py check
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour ouvrir le shell Django
shell() {
    echo -e "${BLUE}Ouverture du shell Django...${NC}"
    python manage.py shell
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour afficher les migrations
showmigrations() {
    echo -e "${BLUE}État des migrations...${NC}"
    python manage.py showmigrations
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Fonction pour reset complet
reset() {
    echo -e "${RED}ATTENTION : Cette opération va supprimer la base de données !${NC}"
    read -p "Êtes-vous sûr ? (oui/non) : " confirm
    if [[ $confirm == "oui" ]]; then
        echo -e "${BLUE}Suppression de la base de données...${NC}"
        if [ -f "db.sqlite3" ]; then
            rm db.sqlite3
        fi
        
        echo -e "${BLUE}Suppression des migrations...${NC}"
        for app in accounts structures plats menus avis; do
            if [ -d "${app}/migrations" ]; then
                find "${app}/migrations" -name "*.py" ! -name "__init__.py" -delete
            fi
        done
        
        echo -e "${BLUE}Recréation des migrations...${NC}"
        python manage.py makemigrations
        
        echo -e "${BLUE}Application des migrations...${NC}"
        python manage.py migrate
        
        echo -e "${GREEN}Reset terminé !${NC}"
    else
        echo -e "${YELLOW}Reset annulé.${NC}"
    fi
    echo
    read -p "Appuyez sur Entrée pour continuer..."
}

# Boucle principale
while true; do
    show_menu
    read -p "Votre choix (1-13) : " choice
    
    case $choice in
        1)
            activate_env
            ;;
        2)
            install_deps
            ;;
        3)
            make_migrations
            ;;
        4)
            migrate
            ;;
        5)
            createsuperuser
            ;;
        6)
            runserver
            ;;
        7)
            runserver_8080
            ;;
        8)
            collectstatic
            ;;
        9)
            check
            ;;
        10)
            shell
            ;;
        11)
            showmigrations
            ;;
        12)
            reset
            ;;
        13)
            echo -e "${GREEN}Au revoir !${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Choix invalide. Veuillez choisir un nombre entre 1 et 13.${NC}"
            echo
            read -p "Appuyez sur Entrée pour continuer..."
            ;;
    esac
done

