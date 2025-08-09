from django.contrib import admin
from .models import Avis

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'date_publication', 'signale')
    list_filter = ('note', 'date_publication', 'signale')
    search_fields = ('user__email', 'commentaire')
    ordering = ('-date_publication',)
    readonly_fields = ('date_publication', 'date_edited')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'note')
        }),
        ('Commentaire', {
            'fields': ('commentaire',)
        }),
        ('Statut', {
            'fields': ('signale',)
        }),
        ('Dates', {
            'fields': ('date_publication', 'date_edited')
        }),
    )
