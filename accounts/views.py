from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, CustomPasswordChangeForm, UserDeleteForm
from accounts.models import UserLoginHistory
from plats.models import Plats
from structures.models import Structures

# Récupère le modèle User personnalisé
User = get_user_model()


def login_view(request):
    # Si l'utilisateur est déjà authentifié, on le redirige
    if request.user.is_authenticated:
        if hasattr(request.user, 'structure') and request.user.structure:
            return redirect('accounts:dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Enregistrement de la tentative de connexion
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

                UserLoginHistory.objects.create(
                    user=user,
                    ip_address=ip_address,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                    login_success=True
                )

                login(request, user)
                messages.success(request, f"Bienvenue {user.first_name}!")
                return redirect('accounts:home')

        # Gestion des échecs de connexion
        email = request.POST.get('username', '')
        try:
            user = User.objects.get(email=email) if email else None
        except User.DoesNotExist:
            user = None

        if user:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

            UserLoginHistory.objects.create(
                user=user,
                ip_address=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                login_success=False
            )

        messages.error(request, "Email ou mot de passe incorrect.")
        return redirect('accounts:login')

    else:
        form = UserLoginForm()

    # Chemin du template: accounts/templates/accounts/login.html
    return render(request, 'accounts/login.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            messages.success(request, "Compte créé avec succès! Vous pouvez maintenant vous connecter.")
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()

    # Chemin du template: accounts/templates/accounts/register_user.html
    return render(request, 'accounts/register_user.html', {'form': form})


@login_required
def dashboard(request):
    structures = Structures.objects.filter(user=request.user)
    login_history = UserLoginHistory.objects.filter(
        user=request.user,
        login_time__gte=timezone.now() - timezone.timedelta(days=10)
    ).order_by('-login_time')

    context = {
        'structures': structures,
        'structures_count': structures.count(),
        'login_history': login_history,
    }

    # Chemin du template: accounts/templates/accounts/dashboard.html
    return render(request, 'accounts/dashboard.html', context)


def home_view(request):
    # Structures
    featured_structures = Structures.objects.all().order_by('-id')[:8]
    villes = Structures.objects.values_list('ville', flat=True).distinct()
    categories = Structures.objects.values_list('type', flat=True).distinct()

    # Plats
    featured_plats = Plats.objects.all().order_by('-id')[:8]
    nom_plats = Plats.objects.values_list('nom', flat=True).distinct()
    plat_categories = Plats.objects.values_list('categorie', flat=True).distinct()
    
    # Plats en promotion
    plats_promotion = Plats.objects.filter(
        en_promotion=True,
        disponibilite=True
    ).filter(
        Q(date_debut_promotion__lte=timezone.now()) | Q(date_debut_promotion__isnull=True)
    ).filter(
        Q(date_fin_promotion__gte=timezone.now()) | Q(date_fin_promotion__isnull=True)
    ).order_by('-date_creation')[:6]

    context = {
        # Structures
        'featured_structures': featured_structures,
        'villes': villes,
        'categories': categories,

        # Plats
        'featured_plats': featured_plats,
        'nom_plats': nom_plats,
        'plat_categories': plat_categories,
        
        # Promotions
        'plats_promotion': plats_promotion,
    }
    return render(request, 'index.html', context)


@login_required
def logout_view(request):
    """Déconnexion de l'utilisateur"""
    if request.user.is_authenticated:
        # Enregistrement de la déconnexion dans l'historique
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        UserLoginHistory.objects.create(
            user=request.user,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
            login_success=True,
            action='LOGOUT'  # Champ optionnel pour différencier connexion/déconnexion
        )

    logout(request)
    return redirect('accounts:login')

@login_required
def profile_update(request):
    """Mise à jour du profil utilisateur"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('accounts:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_form.html', {'form': form})

@login_required
def change_password(request):
    """Changement de mot de passe"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Met à jour la session pour ne pas déconnecter l'utilisateur
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été changé avec succès!')
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def account_delete(request):
    """Suppression du compte utilisateur"""
    if request.method == 'POST':
        form = UserDeleteForm(request.POST)
        if form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, 'Votre compte a été supprimé avec succès.')
            return redirect('accounts:home')
    else:
        form = UserDeleteForm()

    return render(request, 'accounts/account_delete.html', {'form': form})