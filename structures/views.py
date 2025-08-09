from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from menus.models import Menus
from plats.models import Plats
from structures.forms import StructuresRegistrationForm, StructuresUpdateForm
from structures.models import Structures
from django.templatetags.static import static


@login_required(login_url='accounts:login')
def register_structure(request):
    """Vue pour enregistrer une nouvelle structure (réservée aux utilisateurs connectés)"""
    # Si l'utilisateur a déjà une structure, rediriger vers la page de modification
    existing_structure = request.user.structure.first()
    if existing_structure:
        messages.info(request, "Vous avez déjà une structure. Redirection vers la page de modification.")
        return redirect('structures:structure-update', pk=existing_structure.pk)

    if request.method == 'POST':
        form = StructuresRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            structure = form.save(commit=False)
            structure.user = request.user  # Associe la structure à l'utilisateur connecté

            try:
                structure.save()
                messages.success(request, f"La structure {structure.nom} a été créée avec succès!")
                # Redirection vers le dashboard
                return redirect('accounts:dashboard')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")
    else:
        form = StructuresRegistrationForm()

    # Ajout des erreurs non-field dans les messages
    for error in form.non_field_errors():
        messages.error(request, error)

    return render(request, 'structures/register_structure.html', {
        'form': form,
        'structures_count': request.user.structure.count()  # Compte le nombre de structures de l'utilisateur
    })

def list_structures(request):
    """Liste toutes les structures disponibles"""
    featured_structures = Structures.objects.all().order_by('-id')

    # Récupère les villes et catégories uniques pour les filtres
    villes = Structures.objects.order_by('ville').values_list('ville', flat=True).distinct()
    categories = Structures.objects.order_by('type').values_list('type', flat=True).distinct()

    # Plats
    featured_plats = Plats.objects.all().order_by('-id')
    plat_categories = Plats.objects.order_by('categorie').values_list('categorie', flat=True).distinct()


    context = {
        # Structures
        'featured_structures': featured_structures,
        'villes': villes,
        'categories': categories,

        # Plats
        'featured_plats': featured_plats,
        'plat_categories': plat_categories,
    }
    return render(request, 'structures/structure.html', context)

@login_required(login_url='accounts:login')
def structure_detail(request, pk):
    """Détails d'une structure spécifique (accessible seulement par son propriétaire)"""
    structure = get_object_or_404(Structures, pk=pk, user=request.user)
    return render(request, 'structures/structure_detail.html', {'structure': structure})


def detail(request, pk):
    """Détails d'une structure spécifique avec les menus et les plats qui la constituent"""
    structure = get_object_or_404(Structures, pk=pk)
    
    # Récupère tous les plats créés par l'utilisateur qui possède cette structure
    plats = Plats.objects.filter(createur=structure.user)

    # Vérifie si l'utilisateur actuel a des structures
    has_structure = False
    if request.user.is_authenticated:
        has_structure = request.user.structure.exists()

    # Infos avis utilisateur
    from avis.models import Avis
    user_has_avis = False
    user_avis = None
    if request.user.is_authenticated:
        user_avis = Avis.objects.filter(user=request.user, structure=structure).first()
        user_has_avis = user_avis is not None

    # Catégories dynamiques présentes pour cette structure, ordonnées selon les choix du modèle
    order = [k for k, _ in Plats.CATEGORIES]
    present_keys = list(set(plats.values_list('categorie', flat=True)))
    present_keys.sort(key=lambda k: order.index(k) if k in order else len(order))
    label_map = dict(Plats.CATEGORIES)
    categories = [
        {
            'key': key,
            'label': label_map.get(key, key),
        }
        for key in present_keys
    ]

    hero_bg_url = structure.photo.url if structure.photo else static('images/restaurant-bg1.jpg')

    context = {
        'structure': structure,
        'plats': plats,
        'has_structure': has_structure,
        'user_has_avis': user_has_avis,
        'user_avis': user_avis,
        'categories': categories,
        'hero_bg_url': hero_bg_url,
    }
    return render(request, 'structures/detail.html', context)


@login_required(login_url='accounts:login')
def structure_update(request, pk):
    """Mise à jour d'une structure (accessible seulement par son propriétaire)"""
    structure = get_object_or_404(Structures, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StructuresUpdateForm(request.POST, request.FILES, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, 'La structure a été mise à jour avec succès!')
            return redirect('structures:structure-detail', pk=structure.pk)
    else:
        form = StructuresUpdateForm(instance=structure)

    return render(request, 'structures/structure_form.html', {'form': form, 'structure': structure})

@login_required(login_url='accounts:login')
def structure_delete(request, pk):
    """Suppression d'une structure (accessible seulement par son propriétaire)"""
    structure = get_object_or_404(Structures, pk=pk, user=request.user)
    if request.method == 'POST':
        structure.delete()
        messages.success(request, 'La structure a été supprimée avec succès!')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/confirm_delete.html', {'object': structure})

