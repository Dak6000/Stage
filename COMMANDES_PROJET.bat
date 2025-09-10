@echo off
echo ========================================
echo    E-MENU TOGO - COMMANDES PROJET
echo ========================================
echo.

:menu
echo Choisissez une option :
echo.
echo 1. Activer l'environnement virtuel
echo 2. Installer les dépendances
echo 3. Créer les migrations
echo 4. Appliquer les migrations
echo 5. Créer un superutilisateur
echo 6. Démarrer le serveur
echo 7. Démarrer le serveur (port 8080)
echo 8. Collecter les fichiers statiques
echo 9. Vérifier le projet
echo 10. Ouvrir le shell Django
echo 11. Afficher les migrations
echo 12. Reset complet (attention!)
echo 13. Quitter
echo.
set /p choice="Votre choix (1-13) : "

if "%choice%"=="1" goto activate_env
if "%choice%"=="2" goto install_deps
if "%choice%"=="3" goto make_migrations
if "%choice%"=="4" goto migrate
if "%choice%"=="5" goto createsuperuser
if "%choice%"=="6" goto runserver
if "%choice%"=="7" goto runserver_8080
if "%choice%"=="8" goto collectstatic
if "%choice%"=="9" goto check
if "%choice%"=="10" goto shell
if "%choice%"=="11" goto showmigrations
if "%choice%"=="12" goto reset
if "%choice%"=="13" goto exit
goto menu

:activate_env
echo.
echo Activation de l'environnement virtuel...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Environnement virtuel activé !
) else (
    echo Environnement virtuel non trouvé. Création...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Environnement virtuel créé et activé !
)
echo.
pause
goto menu

:install_deps
echo.
echo Installation des dépendances...
pip install -r requirements.txt
echo.
pause
goto menu

:make_migrations
echo.
echo Création des migrations...
python manage.py makemigrations
echo.
pause
goto menu

:migrate
echo.
echo Application des migrations...
python manage.py migrate
echo.
pause
goto menu

:createsuperuser
echo.
echo Création d'un superutilisateur...
python manage.py createsuperuser
echo.
pause
goto menu

:runserver
echo.
echo Démarrage du serveur sur http://127.0.0.1:8000/
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.
python manage.py runserver
goto menu

:runserver_8080
echo.
echo Démarrage du serveur sur http://127.0.0.1:8080/
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.
python manage.py runserver 8080
goto menu

:collectstatic
echo.
echo Collecte des fichiers statiques...
python manage.py collectstatic --noinput
echo.
pause
goto menu

:check
echo.
echo Vérification du projet...
python manage.py check
echo.
pause
goto menu

:shell
echo.
echo Ouverture du shell Django...
python manage.py shell
echo.
pause
goto menu

:showmigrations
echo.
echo État des migrations...
python manage.py showmigrations
echo.
pause
goto menu

:reset
echo.
echo ATTENTION : Cette opération va supprimer la base de données !
set /p confirm="Êtes-vous sûr ? (oui/non) : "
if /i "%confirm%"=="oui" (
    echo Suppression de la base de données...
    if exist "db.sqlite3" del db.sqlite3
    echo Suppression des migrations...
    for /d %%i in (accounts\migrations structures\migrations plats\migrations menus\migrations avis\migrations) do (
        if exist "%%i" (
            for %%j in ("%%i\*.py") do (
                if not "%%~nj"=="__init__" del "%%j"
            )
        )
    )
    echo Recréation des migrations...
    python manage.py makemigrations
    echo Application des migrations...
    python manage.py migrate
    echo Reset terminé !
) else (
    echo Reset annulé.
)
echo.
pause
goto menu

:exit
echo.
echo Au revoir !
pause
exit

