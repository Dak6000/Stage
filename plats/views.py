from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q

from plats.forms import PlatForm, PromotionForm
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
    # Récupérer tous les plats configurés pour être en promotion
    plats = Plats.objects.filter(disponibilite=True).select_related('createur', 'structure')
    plats_promotion = [plat for plat in plats if plat.est_en_promotion()]
    
    # Trier par date de modification/création
    plats_promotion.sort(key=lambda x: (x.date_modification or x.date_creation), reverse=True)
    
    # Catégories uniques pour les filtres
    unique_codes = list(Plats.objects.values_list('categorie', flat=True).distinct())
    label_map = dict(Plats.CATEGORIES)
    plat_categories = [(code, label_map.get(code, code)) for code in unique_codes]
    
    context = {
        'plats_promotion': plats_promotion,
        'plat_categories': plat_categories,
        'title': 'Plats en Promotion'
    }
    return render(request, 'plats/promotion.html', context)

# CRUD pour Plat
@login_required(login_url='accounts:login')
def plat_list(request):
    plats = Plats.objects.filter(createur=request.user).order_by('-date_modification', '-date_creation')
    
    # Recherche par nom
    search_query = request.GET.get('search', '')
    if search_query:
        plats = plats.filter(nom__icontains=search_query)
    
    # Filtres avancés
    categorie_filter = request.GET.get('categorie', '')
    disponibilite_filter = request.GET.get('disponibilite', '')
    promotion_filter = request.GET.get('promotion', '')
    
    if categorie_filter:
        plats = plats.filter(categorie=categorie_filter)
    
    if disponibilite_filter != '':
        plats = plats.filter(disponibilite=disponibilite_filter == 'True')
    
    if promotion_filter != '':
        if promotion_filter == 'True':
            plats = plats.filter(en_promotion=True)
        elif promotion_filter == 'False':
            plats = plats.filter(en_promotion=False)
    
    return render(request, 'plats/list.html', {
        'plats': plats,
        'search_query': search_query,
        'categorie_filter': categorie_filter,
        'disponibilite_filter': disponibilite_filter,
        'promotion_filter': promotion_filter,
        'categories': Plats.CATEGORIES,
    })

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

# Vue pour configurer la promotion d'un plat
@login_required
def promotion_form(request, pk):
    plat = get_object_or_404(Plats, pk=pk, createur=request.user)
    
    if request.method == 'POST':
        form = PromotionForm(request.POST, instance=plat)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Promotion configurée avec succès!')
                return redirect('plats:plat-list')
            except Exception as e:
                messages.error(request, f'Une erreur est survenue: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label if field in form.fields else field}: {error}")
    else:
        form = PromotionForm(instance=plat)

    context = {
        'form': form,
        'plat': plat,
        'title': 'Configurer la promotion'
    }
    return render(request, 'plats/promotion_form.html', context)

# Vue pour activer/désactiver la promotion d'un plat
@login_required
def toggle_promotion(request, pk):
    plat = get_object_or_404(Plats, pk=pk, createur=request.user)
    
    if plat.en_promotion:
        # Si la promotion est active, on la désactive
        plat.en_promotion = False
        plat.prix_promotionnel = None
        plat.pourcentage_reduction = None
        plat.date_debut_promotion = None
        plat.heure_debut_promotion = None
        plat.date_fin_promotion = None
        plat.heure_fin_promotion = None
        plat.description_promotion = ''
        plat.save()
        messages.success(request, 'Promotion désactivée avec succès!')
    else:
        # Si la promotion n'est pas active, on redirige vers le formulaire de configuration
        return redirect('plats:promotion-form', pk=pk)
    
    return redirect('plats:plat-list')