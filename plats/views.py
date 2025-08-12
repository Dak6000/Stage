from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q

from plats.forms import PlatForm
from avis.models import Avis
from plats.models import Plats

User = get_user_model()

# Vue publique pour voir les détails d'un plat
def plat_detail(request, pk):
    plat = get_object_or_404(Plats, pk=pk)
    
    # Trouver le premier menu contenant ce plat (pour le bouton de retour)
    menu_parent = None
    # Infos avis utilisateur
    user_has_avis = False
    user_avis = None
    if request.user.is_authenticated:
        menu_parent = plat.menus.first()
        user_avis = Avis.objects.filter(user=request.user, plat=plat).first()
        user_has_avis = user_avis is not None
    context = {
        'plat': plat,
        'menu_parent': menu_parent,
        'temps_total': plat.get_temps_total(),
        'prix_affichage': plat.get_prix_affichage(),
        'user_has_avis': user_has_avis,
        'user_avis': user_avis,
    }
    return render(request, 'plats/detail.html', context)

# Vue publique pour voir les plats en promotion
def plats_promotion(request):
    plats_promotion = Plats.objects.filter(
        en_promotion=True,
        disponibilite=True
    ).filter(
        Q(date_debut_promotion__lte=timezone.now()) | Q(date_debut_promotion__isnull=True)
    ).filter(
        Q(date_fin_promotion__gte=timezone.now()) | Q(date_fin_promotion__isnull=True)
    )
    
    context = {
        'plats_promotion': plats_promotion,
        'title': 'Plats en Promotion'
    }
    return render(request, 'plats/promotion.html', context)

# CRUD pour Plat
@login_required(login_url='accounts:login')
def plat_list(request):
    plats = Plats.objects.filter(createur=request.user)
    return render(request, 'plats/list.html', {'plats': plats})

@login_required(login_url='accounts:login')
def plat_create(request):
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                plat = form.save(commit=False)
                plat.createur = request.user
                # Rattacher la structure du créateur si elle existe
                user_structure = request.user.structure.first()
                if not user_structure:
                    messages.error(request, "Vous devez d'abord créer votre structure avant d'ajouter un plat.")
                    return redirect('structures:register-structure')
                plat.structure = user_structure
                
                # Sauvegarde des dates/heures de promotion
                date_heure_debut = form.cleaned_data.get('date_heure_debut_promotion')
                date_heure_fin = form.cleaned_data.get('date_heure_fin_promotion')
                
                if date_heure_debut:
                    plat.date_debut_promotion = date_heure_debut.date()
                    plat.heure_debut_promotion = date_heure_debut.time().strftime('%H:%M')
                
                if date_heure_fin:
                    plat.date_fin_promotion = date_heure_fin.date()
                    plat.heure_fin_promotion = date_heure_fin.time().strftime('%H:%M')
                
                plat.save()
                messages.success(request, 'Plat créé avec succès!')
                return redirect('plats:plat-list')
            except Exception as e:
                messages.error(request, f'Une erreur est survenue: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label if field in form.fields else field}: {error}")
    else:
        form = PlatForm()

    context = {
        'form': form,
        'title': 'Créer un plat',
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M')
    }
    return render(request, 'plats/form.html', context)

@login_required(login_url='accounts:login')
def plat_update(request, pk):
    plat = get_object_or_404(Plats, pk=pk, createur=request.user)

    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES, instance=plat)
        if form.is_valid():
            try:
                plat = form.save(commit=False)
                plat.structure = request.user.structure.first()
                
                # Gestion des dates/heures de promotion
                date_heure_debut = form.cleaned_data.get('date_heure_debut_promotion')
                date_heure_fin = form.cleaned_data.get('date_heure_fin_promotion')
                
                if date_heure_debut:
                    plat.date_debut_promotion = date_heure_debut.date()
                    plat.heure_debut_promotion = date_heure_debut.time().strftime('%H:%M')
                else:
                    plat.date_debut_promotion = None
                    plat.heure_debut_promotion = None
                
                if date_heure_fin:
                    plat.date_fin_promotion = date_heure_fin.date()
                    plat.heure_fin_promotion = date_heure_fin.time().strftime('%H:%M')
                else:
                    plat.date_fin_promotion = None
                    plat.heure_fin_promotion = None
                
                plat.save()
                messages.success(request, 'Plat mis à jour avec succès!')
                return redirect('plats:plat-list')
            except Exception as e:
                messages.error(request, f'Une erreur est survenue: {str(e)}')
    else:
        form = PlatForm(instance=plat)

    context = {
        'form': form,
        'title': 'Modifier le plat',
        'now': timezone.now().strftime('%Y-%m-%dT%H:%M')
    }
    return render(request, 'plats/form.html', context)

@login_required(login_url='accounts:login')
def plat_delete(request, pk):
    plats = get_object_or_404(Plats, pk=pk, createur=request.user)
    if request.method == 'POST':
        plats.delete()
        messages.success(request, 'Plat supprimé avec succès!')
        return redirect('plats:plat-list')
    return render(request, 'plats/confirm_delete.html', {'object': plats})

# Vue pour activer/désactiver la promotion d'un plat
@login_required
def toggle_promotion(request, pk):
    plat = get_object_or_404(Plats, pk=pk)
    
    # Basculer l'état de promotion
    plat.en_promotion = not plat.en_promotion
    
    # Si on désactive la promotion, on peut aussi réinitialiser les champs
    if not plat.en_promotion:
        plat.prix_promotionnel = None
        plat.pourcentage_reduction = None
    
    plat.save()
    return redirect('plats:plat-list')  # Rediriger vers la liste des plats