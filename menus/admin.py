from django.contrib import admin
from .models import Menus

@admin.register(Menus)
class MenusAdmin(admin.ModelAdmin):
    list_display = ('nom', 'structure', 'status', 'createur')
    list_filter = ('status', 'structure')
    search_fields = ('nom', 'structure__nom', 'createur__email')
    ordering = ('-date_creation',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'status')
        }),
        ('Relations', {
            'fields': ('structure', 'createur')
        }),
        ('Plats', {
            'fields': ('plats',)
        }),
    )

