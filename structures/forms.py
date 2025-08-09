from django import forms
from django.core.exceptions import ValidationError
from structures.models import Structures
import re


class StructuresRegistrationForm(forms.ModelForm):
    heure_ouverture = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        help_text="Format: HH:MM"
    )

    heure_fermeture = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        help_text="Format: HH:MM"
    )

    class Meta:
        model = Structures
        fields = ['nom', 'telephone', 'adresse', 'ville', 'heure_ouverture', 'heure_fermeture', 'description', 'type',
                  'photo']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la structure',
                'aria-describedby': 'nomHelp'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone',
                'aria-describedby': 'telephoneHelp'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse',
                'aria-describedby': 'adresseHelp'
            }),
            'type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type de structure',
                'aria-describedby': 'typeHelp'
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville',
                'aria-describedby': 'villeHelp'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
                'aria-describedby': 'descriptionHelp'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'aria-describedby': 'photoHelp'
            }),
        }
        help_texts = {
            'nom': 'Le nom doit être unique et contenir au moins 3 caractères.',
            'telephone': 'Format: +228XXXXXXXX ou XXXXXXXX',
            'photo': 'Image de présentation de votre structure (format JPG/PNG)',
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not re.match(r'^(\+228|)[0-9]{8,10}$', telephone):
            raise ValidationError("Numéro de téléphone invalide. Format attendu: +228XXXXXXXX ou XXXXXXXX")
        return telephone

    def clean(self):
        cleaned_data = super().clean()
        heure_ouverture = cleaned_data.get('heure_ouverture')
        heure_fermeture = cleaned_data.get('heure_fermeture')

        if heure_ouverture and heure_fermeture and heure_ouverture >= heure_fermeture:
            self.add_error('heure_fermeture', "L'heure de fermeture doit être après l'heure d'ouverture")

        return cleaned_data


class StructuresUpdateForm(StructuresRegistrationForm):
    class Meta(StructuresRegistrationForm.Meta):
        fields = ['nom', 'telephone', 'adresse', 'ville', 'heure_ouverture', 'heure_fermeture',
                  'description', 'type', 'photo', 'featured']
        widgets = {
            **StructuresRegistrationForm.Meta.widgets,
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StructuresDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Je confirme vouloir supprimer ma structure définitivement",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )