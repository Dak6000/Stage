from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    #path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path("", include("accounts.urls", namespace="accounts")),
    path("menus/", include("menus.urls", namespace="menus")),
    path("avis/", include("avis.urls", namespace="avis")),
    path("plats/", include("plats.urls", namespace="plats")),
    path("promotions/", include("promotions.urls", namespace="promotions")),
    path("structures/", include("structures.urls", namespace="structures")),
]
