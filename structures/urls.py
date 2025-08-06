from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # Importez vos vues depuis accounts/views.py

app_name = 'structures'  # Namespace pour les URLs

urlpatterns = [
    # Authentification
    path('register_structure/', views.register_structure, name='register_structure'),
    path('structure/', views.list_structures, name='structure'),

    # URLs de gestion des structures
    path('structure_detail/<int:pk>/', views.structure_detail, name='structure-detail'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('structure_form/<int:pk>/', views.structure_update, name='structure-update'),
    path('account_delete/<int:pk>/', views.structure_delete, name='structure-delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)