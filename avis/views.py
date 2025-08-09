from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Avis
from .forms import AvisForm
from structures.models import Structures
from plats.models import Plats

@login_required
def avis_list(request):
    """Liste des avis de l'utilisateur connecté"""
    avis_user = Avis.objects.filter(user=request.user).order_by('-date_publication')
    
    # Pagination
    paginator = Paginator(avis_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'avis_count': avis_user.count(),
    }
    return render(request, 'avis/avis_list.html', context)

@login_required
def avis_structure_list(request, structure_id):
    """Liste des avis d'une structure (pour le propriétaire)"""
    structure = get_object_or_404(Structures, pk=structure_id, user=request.user)
    avis_structure = Avis.objects.filter(structure=structure).order_by('-date_publication')
    
    # Pagination
    paginator = Paginator(avis_structure, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'structure': structure,
        'page_obj': page_obj,
        'avis_count': avis_structure.count(),
    }
    return render(request, 'avis/avis_structure_list.html', context)

@login_required
def avis_create_structure(request, structure_id):
    """Créer un avis pour une structure"""
    structure = get_object_or_404(Structures, pk=structure_id)
    
    # Vérifier si l'utilisateur a déjà laissé un avis
    existing_avis = Avis.objects.filter(user=request.user, structure=structure)
    if existing_avis.exists():
        messages.warning(request, "Vous avez déjà laissé un avis pour cette structure.")
        return redirect('structures:detail', pk=structure_id)
    
    if request.method == 'POST':
        # Lier explicitement l'instance pour fiabiliser la validation
        form = AvisForm(request.POST, user=request.user, instance=Avis(user=request.user, structure=structure))
        if form.is_valid():
            avis = form.save(commit=False)
            avis.user = request.user
            avis.structure = structure
            avis.plat = None
            avis.save()
            messages.success(request, "Votre avis a été publié avec succès!")
            return redirect('structures:detail', pk=structure_id)
    else:
        form = AvisForm(user=request.user, instance=Avis(user=request.user, structure=structure))
    
    context = {
        'form': form,
        'structure': structure,
        'title': f'Avis sur {structure.nom}'
    }
    return render(request, 'avis/avis_form.html', context)

@login_required
def avis_create_plat(request, plat_id):
    """Créer un avis pour un plat"""
    plat = get_object_or_404(Plats, pk=plat_id)
    
    # Vérifier si l'utilisateur a déjà laissé un avis
    existing_avis = Avis.objects.filter(user=request.user, plat=plat)
    if existing_avis.exists():
        messages.warning(request, "Vous avez déjà laissé un avis pour ce plat.")
        return redirect('plats:plat-detail', pk=plat_id)
    
    if request.method == 'POST':
        # Lier explicitement l'instance pour fiabiliser la validation
        form = AvisForm(request.POST, user=request.user, instance=Avis(user=request.user, plat=plat))
        if form.is_valid():
            avis = form.save(commit=False)
            avis.user = request.user
            avis.plat = plat
            avis.structure = None
            avis.save()
            messages.success(request, "Votre avis a été publié avec succès!")
            return redirect('plats:plat-detail', pk=plat_id)
    else:
        form = AvisForm(user=request.user, instance=Avis(user=request.user, plat=plat))
    
    context = {
        'form': form,
        'plat': plat,
        'title': f'Avis sur {plat.nom}'
    }
    return render(request, 'avis/avis_form.html', context)

@login_required
def avis_update(request, avis_id):
    """Modifier un avis"""
    avis = get_object_or_404(Avis, pk=avis_id, user=request.user)
    
    if request.method == 'POST':
        form = AvisForm(request.POST, instance=avis, user=request.user)
        if form.is_valid():
            avis_obj = form.save(commit=False)
            avis_obj.user = request.user
            # Préserver le lien structure/plat existant si non modifié par le formulaire
            if avis_obj.structure and avis_obj.plat:
                # Sécurité: ne jamais avoir les deux
                avis_obj.plat = None
            avis_obj.save()
            messages.success(request, "Votre avis a été mis à jour avec succès!")
            
            # Rediriger vers la bonne page
            if avis.structure:
                return redirect('structures:structure-detail', pk=avis.structure.pk)
            elif avis.plat:
                return redirect('plats:plat-detail', pk=avis.plat.pk)
    else:
        form = AvisForm(instance=avis, user=request.user)
    
    context = {
        'form': form,
        'avis': avis,
        'title': 'Modifier votre avis'
    }
    return render(request, 'avis/avis_form.html', context)

@login_required
def avis_delete(request, avis_id):
    """Supprimer un avis"""
    avis = get_object_or_404(Avis, pk=avis_id, user=request.user)
    
    if request.method == 'POST':
        # Sauvegarder les références avant suppression
        structure_pk = avis.structure.pk if avis.structure else None
        plat_pk = avis.plat.pk if avis.plat else None
        
        avis.delete()
        messages.success(request, "Votre avis a été supprimé avec succès!")
        
        # Rediriger vers la bonne page
        if structure_pk:
            return redirect('structures:structure-detail', pk=structure_pk)
        elif plat_pk:
            return redirect('plats:plat-detail', pk=plat_pk)
    
    context = {
        'avis': avis,
        'title': 'Supprimer votre avis'
    }
    return render(request, 'avis/avis_confirm_delete.html', context)

@login_required
@require_POST
def avis_signal(request, avis_id):
    """Signaler un avis"""
    avis = get_object_or_404(Avis, pk=avis_id)
    
    if avis.user == request.user:
        messages.error(request, "Vous ne pouvez pas signaler votre propre avis.")
    else:
        avis.signale = True
        avis.save()
        messages.success(request, "L'avis a été signalé avec succès.")
    
    # Rediriger vers la page précédente
    if avis.structure:
        return redirect('structures:structure-detail', pk=avis.structure.pk)
    elif avis.plat:
        return redirect('plats:plat-detail', pk=avis.plat.pk)

def avis_structure_public(request, structure_id):
    """Afficher les avis publics d'une structure"""
    structure = get_object_or_404(Structures, pk=structure_id)
    avis_structure = Avis.objects.filter(structure=structure, signale=False).order_by('-date_publication')
    
    # Vérifier si l'utilisateur connecté a déjà laissé un avis
    user_has_avis = False
    user_avis = None
    if request.user.is_authenticated:
        user_avis = Avis.objects.filter(user=request.user, structure=structure).first()
        user_has_avis = user_avis is not None
    
    # Pagination
    paginator = Paginator(avis_structure, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'structure': structure,
        'page_obj': page_obj,
        'avis_count': avis_structure.count(),
        'user_has_avis': user_has_avis,
        'user_avis': user_avis,
    }
    return render(request, 'avis/avis_structure_public.html', context)

def avis_plat_public(request, plat_id):
    """Afficher les avis publics d'un plat"""
    plat = get_object_or_404(Plats, pk=plat_id)
    avis_plat = Avis.objects.filter(plat=plat, signale=False).order_by('-date_publication')
    
    # Vérifier si l'utilisateur connecté a déjà laissé un avis
    user_has_avis = False
    user_avis = None
    if request.user.is_authenticated:
        user_avis = Avis.objects.filter(user=request.user, plat=plat).first()
        user_has_avis = user_avis is not None
    
    # Pagination
    paginator = Paginator(avis_plat, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'plat': plat,
        'page_obj': page_obj,
        'avis_count': avis_plat.count(),
        'user_has_avis': user_has_avis,
        'user_avis': user_avis,
    }
    return render(request, 'avis/avis_plat_public.html', context)
