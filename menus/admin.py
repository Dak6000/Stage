from django.contrib import admin
from .models import Menus, MenuPlat

class MenuPlatInline(admin.TabularInline):
    model = MenuPlat
    extra = 1
    autocomplete_fields = ['plat']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Restreindre la liste des plats à ceux du même créateur que le menu
        if db_field.name == 'plat' and getattr(request, 'resolver_match', None):
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                try:
                    menu = Menus.objects.get(pk=obj_id)
                    kwargs['queryset'] = menu.createur.plats_set.all() if hasattr(menu.createur, 'plats_set') else menu.createur.plats_set.none()
                except Menus.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Menus)
class MenusAdmin(admin.ModelAdmin):
    list_display = ('nom', 'structure', 'status', 'createur')
    list_filter = ('status', 'structure')
    search_fields = ('nom', 'structure__nom', 'createur__email')
    ordering = ('-date_creation',)
    inlines = [MenuPlatInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'status')
        }),
        ('Relations', {
            'fields': ('structure', 'createur')
        }),
    )

