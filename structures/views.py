from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from menus.models import Menus
from plats.models import Plats
from structures.forms import StructuresRegistrationForm, StructuresUpdateForm
from structures.models import Structures


@login_required
def register_structure(request):
    """Vue pour enregistrer une nouvelle structure (réservée aux utilisateurs connectés)"""
    if request.method == 'POST':
        form = StructuresRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            structure = form.save(commit=False)
            structure.user = request.user  # Associe la structure à l'utilisateur connecté

            try:
                structure.save()
                messages.success(request, f"La structure {structure.nom} a été créée avec succès!")
                # Redirection vers la page précédente ou le dashboard
                return redirect('accounts:dashboard')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = StructuresRegistrationForm()

    return render(request, 'structures/register_structure.html', {
        'form': form,
        'structures_count': request.user.structure.count()  # Compte le nombre de structures de l'utilisateur
    })

def list_structures(request):
    """Liste toutes les structures disponibles"""
    featured_structures = Structures.objects.all().order_by('-id')

    # Récupère les villes et catégories uniques pour les filtres
    villes = Structures.objects.values_list('ville', flat=True).distinct()
    categories = Structures.objects.values_list('type', flat=True).distinct()

    # Plats
    featured_plats = Plats.objects.all().order_by('-id')
    plat_categories = Plats.objects.values_list('categorie', flat=True).distinct()


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

@login_required
def structure_detail(request, pk):
    """Détails d'une structure spécifique (accessible seulement par son propriétaire)"""
    structure = get_object_or_404(Structures, pk=pk, user=request.user)
    return render(request, 'structures/structure_detail.html', {'structure': structure})


@login_required(login_url='accounts:login')
def detail(request, pk):
    """Détails d'une structure spécifique avec les menus et les plats qui la constituent"""
    structure = get_object_or_404(Structures, pk=pk)
    menus = Menus.objects.filter(structure=structure).prefetch_related('plats')

    # Vérifie si l'utilisateur actuel est le propriétaire de la structure
    is_owner = request.user == structure.user

    context = {
        'structure': structure,
        'menus': menus,
        'has_structure': is_owner,  # Utilisez ce booléen dans votre template pour conditionner l'affichage
    }
    return render(request, 'structures/detail.html', context)


@login_required
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

@login_required
def structure_delete(request, pk):
    """Suppression d'une structure (accessible seulement par son propriétaire)"""
    structure = get_object_or_404(Structures, pk=pk, user=request.user)
    if request.method == 'POST':
        structure.delete()
        messages.success(request, 'La structure a été supprimée avec succès!')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/confirm_delete.html', {'object': structure})

