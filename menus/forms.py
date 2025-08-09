from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from menus.models import Menus
from plats.models import Plats

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
    plats = forms.ModelMultipleChoiceField(
        queryset=Plats.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Plats"
    )

    class Meta:
        model = Menus
        fields = ['nom', 'status', 'plats']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Restreindre les plats au propriétaire
        if user is not None:
            self.fields['plats'].queryset = Plats.objects.filter(createur=user)
        else:
            self.fields['plats'].queryset = Plats.objects.none()
        # Pré-sélectionner les plats déjà associés lors d'une édition
        if getattr(self, 'instance', None) and getattr(self.instance, 'pk', None):
            self.initial['plats'] = self.instance.plats.all()

