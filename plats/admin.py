from django.contrib import admin
from .models import Plats

@admin.register(Plats)
class PlatsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'createur', 'disponibilite')
    list_filter = ('categorie', 'disponibilite', 'createur')
    search_fields = ('nom', 'description', 'createur__email')
    ordering = ('-id',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'description', 'categorie', 'prix')
        }),
        ('Créateur', {
            'fields': ('createur',)
        }),
        ('Disponibilité', {
            'fields': ('disponibilite',)
        }),
        ('Médias', {
            'fields': ('photo',)
        }),
    )
