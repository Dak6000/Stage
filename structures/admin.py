from django.contrib import admin
from .models import Structures

@admin.register(Structures)
class StructuresAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'ville', 'user', 'featured', 'date_creation')
    list_filter = ('type', 'featured', 'date_creation', 'ville')
    search_fields = ('nom', 'description', 'adresse', 'ville', 'user__email')
    ordering = ('-date_creation',)
    readonly_fields = ('date_creation',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'description', 'type', 'user')
        }),
        ('Localisation', {
            'fields': ('adresse', 'ville', 'telephone')
        }),
        ('Horaires', {
            'fields': ('heure_ouverture', 'heure_fermeture')
        }),
        ('Médias', {
            'fields': ('photo',)
        }),
        ('Statut', {
            'fields': ('featured', 'date_creation')
        }),
    )
