from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from plats.forms import PlatForm
from plats.models import Plats

User = get_user_model()

# CRUD pour Plat
@login_required
def plat_list(request):
    plats = Plats.objects.filter(createur=request.user)
    return render(request, 'plats/list.html', {'plats': plats})

@login_required
def plat_create(request):
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            plats = form.save(commit=False)
            plats.createur = request.user  # Ici request.user est déjà une instance de votre User personnalisé
            plats.save()
            messages.success(request, 'Plat créé avec succès!')
            return redirect('plats:plat-list')
    else:
        form = PlatForm()
    return render(request, 'plats/form.html', {'form': form, 'title': 'Créer un plat'})

@login_required
def plat_update(request, pk):
    plats = get_object_or_404(Plats, pk=pk, createur=request.user)
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES, instance=plats)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plat mis à jour avec succès!')
            return redirect('plats:plat-list')
    else:
        form = PlatForm(instance=plats)
    return render(request, 'plats/form.html', {'form': form, 'title': 'Modifier le plat'})

@login_required
def plat_delete(request, pk):
    plats = get_object_or_404(Plats, pk=pk, createur=request.user)
    if request.method == 'POST':
        plats.delete()
        messages.success(request, 'Plat supprimé avec succès!')
        return redirect('plats:plat-list')
    return render(request, 'plats/confirm_delete.html', {'object': plats})