from django import forms

from structures.models import Structures


class StructuresRegistrationForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=Structures.TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Structures
        fields = ['nom', 'telephone', 'adresse', 'ville', 'heure_ouverture', 'heure_fermeture', 'description', 'type', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la structure'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'heure_ouverture': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM'}),
            'heure_fermeture': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class StructuresUpdateForm(forms.ModelForm):
    class Meta:
        model = Structures
        fields = ['nom', 'telephone', 'adresse', 'ville', 'heure_ouverture', 'heure_fermeture', 'description', 'type', 'photo', 'featured']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'heure_ouverture': forms.TextInput(attrs={'class': 'form-control'}),
            'heure_fermeture': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StructuresDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Je confirme vouloir supprimer ma structure définitivement",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )