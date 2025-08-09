from django.urls import path
from . import views

app_name = "avis"

urlpatterns = [
    # Avis de l'utilisateur
    path('', views.avis_list, name='avis-list'),
    
    # Avis sur les structures
    path('structure/<int:structure_id>/', views.avis_structure_public, name='avis-structure-public'),
    path('structure/<int:structure_id>/create/', views.avis_create_structure, name='avis-create-structure'),
    path('structure/<int:structure_id>/list/', views.avis_structure_list, name='avis-structure-list'),
    
    # Avis sur les plats
    path('plat/<int:plat_id>/', views.avis_plat_public, name='avis-plat-public'),
    path('plat/<int:plat_id>/create/', views.avis_create_plat, name='avis-create-plat'),
    
    # Gestion des avis
    path('<int:avis_id>/update/', views.avis_update, name='avis-update'),
    path('<int:avis_id>/delete/', views.avis_delete, name='avis-delete'),
    path('<int:avis_id>/signal/', views.avis_signal, name='avis-signal'),
]