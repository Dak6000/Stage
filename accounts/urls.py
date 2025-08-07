from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # Importez vos vues depuis accounts/views.py

app_name = 'accounts'  # Namespace pour les URLs

urlpatterns = [
    # Page d'accueil (racine du site)
    path('', views.home_view, name='home'),

    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # URLs de profil utilisateur
    path('profile_form', views.profile_update, name='profile-update'),
    path('change_password', views.change_password, name='password-change'),
    path('account_delete', views.account_delete, name='account-delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)