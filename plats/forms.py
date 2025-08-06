from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from plats.models import Plats

User = get_user_model()

class PlatForm(forms.ModelForm):
    nom = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du plat'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Description détaillée du plat'
        })
    )
    prix = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix (en Fcfa)',
            'step': '0.01'
        })
    )
    categorie = forms.ChoiceField(
        choices=Plats.CATEGORIES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    disponibilite = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        initial=True
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Plats
        fields = ['nom', 'description', 'prix', 'categorie', 'disponibilite', 'photo']

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix <= 0:
            raise ValidationError("Le prix doit être supérieur à zéro.")
        return prix