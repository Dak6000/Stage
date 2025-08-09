from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from menus.models import Menus

User = get_user_model()

class MenuForm(forms.ModelForm):
    nom = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du menu'
        })
    )
    status = forms.ChoiceField(
        choices=Menus.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    # On ne sélectionne plus des plats ici (1 plat -> 1 menu)
    # L'ajout de plats se fait via le formulaire des plats

    class Meta:
        model = Menus
        fields = ['nom', 'status']

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

