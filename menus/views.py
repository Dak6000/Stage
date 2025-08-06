from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from menus.forms import MenuForm
from menus.models import Menus

User = get_user_model()

# CRUD pour Menu
@login_required
def menu_list(request):
    menus = Menus.objects.filter(createur=request.user)
    return render(request, 'menus/list.html', {'menus': menus})


@login_required
def menu_create(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, user=request.user)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.createur = request.user
            # Associer automatiquement à la structure de l'utilisateur
            menu.structure = request.user.structure.first()
            menu.save()
            form.save_m2m()  # Pour sauvegarder les relations many-to-many
            messages.success(request, 'Menu créé avec succès!')
            return redirect('menus:menus-list')
    else:
        form = MenuForm(user=request.user)

    return render(request, 'menus/form.html', {
        'form': form,
        'title': 'Créer un menu'
    })

@login_required
def menu_update(request, pk):
    menu = get_object_or_404(Menus, pk=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu, user=request.user)
        if form.is_valid():
            menu = form.save()  # Sauvegarde l'instance principale
            messages.success(request, 'Le menu a été mis à jour avec succès.')
            return redirect('menus:menus-list')
    else:
        form = MenuForm(instance=menu, user=request.user)

    return render(request, 'menus/form.html', {'form': form, 'title': 'Modifier un menu'})

@login_required
def menu_delete(request, pk):
    menu = get_object_or_404(Menus, pk=pk, createur=request.user)
    if request.method == 'POST':
        menu.delete()
        messages.success(request, 'Menu supprimé avec succès!')
        return redirect('menus:menus-list')
    return render(request, 'menus/confirm_delete.html', {'object': menu})
