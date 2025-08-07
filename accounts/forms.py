from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),  # Utilisation de gettext pour l'internationalisation
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Votre email'),
            'autofocus': True,
            'autocomplete': 'email'  # Ajout pour une meilleure expérience utilisateur
        })
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Votre mot de passe'),
            'autocomplete': 'current-password'
        }),
        strip=False  # Important pour ne pas supprimer les espaces accidentels
    )

    error_messages = {
        'invalid_login': _("Email ou mot de passe incorrect."),
        'inactive': _("Ce compte est inactif."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'aria-describedby': 'passwordHelp'
        })

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        # Vérification supplémentaire du statut si nécessaire
        if user.status == 'suspended':
            raise forms.ValidationError(
                "Ce compte a été suspendu.",
                code='suspended',
            )

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe (min. 8 caractères)'
        }),
        help_text="Au moins 8 caractères, pas uniquement des chiffres."
    )
    password2 = forms.CharField(
        label="Confirmation",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe'
        })
    )
    first_name = forms.CharField(  # Utilisation de first_name au lieu de prenom
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        })
    )
    last_name = forms.CharField(  # Utilisation de last_name au lieu de nom
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'telephone', 'adresse', 'ville', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ancien mot de passe'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'})
    )

class UserDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Je confirme vouloir supprimer mon compte définitivement",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )