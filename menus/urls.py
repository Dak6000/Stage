from django.urls import path
from . import views

app_name = 'menus'

urlpatterns = [
    # Menus
    path('menus/', views.menu_list, name='menus-list'),
    path('menus/nouveau/', views.menu_create, name='menus-create'),
    path('menus/<int:pk>/modifier/', views.menu_update, name='menus-update'),
    path('menus/<int:pk>/supprimer/', views.menu_delete, name='menus-delete'),
    path('<int:pk>/', views.menu_detail, name='menu-detail'),
]