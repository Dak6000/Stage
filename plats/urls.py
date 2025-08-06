from django.urls import path
from . import views

app_name = 'plats'

urlpatterns = [
    # Plats
    path('plats/', views.plat_list, name='plat-list'),
    path('plats/nouveau/', views.plat_create, name='plat-create'),
    path('plats/<int:pk>/modifier/', views.plat_update, name='plat-update'),
    path('plats/<int:pk>/supprimer/', views.plat_delete, name='plat-delete'),

]