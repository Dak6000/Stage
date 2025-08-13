from django.urls import path
from . import views

app_name = 'plats'

urlpatterns = [
    # Plats
    path('plats/', views.plat_list, name='plat-list'),
    path('plats/<int:pk>/', views.plat_detail, name='plat-detail'),
    path('plats/nouveau/', views.plat_create, name='plat-create'),
    path('plats/<int:pk>/modifier/', views.plat_update, name='plat-update'),
    path('plats/<int:pk>/supprimer/', views.plat_delete, name='plat-delete'),
    
    # Promotions
    path('promotions/', views.plats_promotion, name='plats-promotion'),
    path('plats/<int:pk>/toggle-promotion/', views.toggle_promotion, name='toggle-promotion'),
    path('plats/<int:pk>/promotion/', views.promotion_form, name='promotion-form'),
]