from django import forms
from django.core.exceptions import ValidationError
from .models import Avis

class AvisForm(forms.ModelForm):
    # Utiliser TypedChoiceField pour convertir la valeur POST (string) en int
    note = forms.TypedChoiceField(
        choices=Avis.NOTE_CHOICES,
        coerce=int,
        label="Note",
        empty_value=None,
        widget=forms.HiddenInput(),  # on gère l'UI des étoiles manuellement dans le template
    )

    # Champs cachés pour fiabiliser le lien en POST
    structure_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    plat_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    commentaire = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Partagez votre expérience...'
        }),
        label="Commentaire",
        max_length=1000,
        help_text="Maximum 1000 caractères"
    )

    class Meta:
        model = Avis
        fields = ['note', 'commentaire']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.structure = kwargs.pop('structure', None)
        self.plat = kwargs.pop('plat', None)
        super().__init__(*args, **kwargs)

        # Préserver les liaisons structure/plat depuis l'instance (même sans pk)
        if getattr(self, 'instance', None) is not None:
            if self.structure is None and self.plat is None:
                self.structure = getattr(self.instance, 'structure', None)
                self.plat = getattr(self.instance, 'plat', None)

        # Initialiser les champs cachés
        if self.structure is not None:
            self.fields['structure_id'].initial = getattr(self.structure, 'pk', None)
        if self.plat is not None:
            self.fields['plat_id'].initial = getattr(self.plat, 'pk', None)

        # S'assurer que l'instance portée par le ModelForm est déjà liée
        if getattr(self, 'instance', None) is not None:
            self.instance.structure = self.structure
            self.instance.plat = self.plat
        
        # Personnaliser les labels selon le type
        if self.structure:
            self.fields['commentaire'].label = f"Commentaire sur {self.structure.nom}"
        elif self.plat:
            self.fields['commentaire'].label = f"Commentaire sur {self.plat.nom}"

    def clean(self):
        cleaned_data = super().clean()

        # Récupérer les liaisons depuis les champs cachés si non fournies
        try:
            if self.structure is None and cleaned_data.get('structure_id'):
                from structures.models import Structures
                self.structure = Structures.objects.get(pk=cleaned_data['structure_id'])
            if self.plat is None and cleaned_data.get('plat_id'):
                from plats.models import Plats
                self.plat = Plats.objects.get(pk=cleaned_data['plat_id'])
        except Exception:
            # Laisser le validateur modèle/form gérer un message plus explicite si besoin
            pass

        # Propager sur l'instance avant la validation du modèle
        if getattr(self, 'instance', None) is not None:
            self.instance.structure = self.structure
            self.instance.plat = self.plat

        # Vérifier si l'utilisateur a déjà laissé un avis
        if self.user:
            if self.structure:
                existing_avis = Avis.objects.filter(user=self.user, structure=self.structure)
            elif self.plat:
                existing_avis = Avis.objects.filter(user=self.user, plat=self.plat)
            else:
                raise ValidationError("Une structure ou un plat doit être spécifié.")

            # En mode édition, ignorer l'avis courant
            if getattr(self, 'instance', None) and getattr(self.instance, 'pk', None):
                existing_avis = existing_avis.exclude(pk=self.instance.pk)

            if existing_avis.exists():
                raise ValidationError("Vous avez déjà laissé un avis pour cet élément.")
        
        return cleaned_data

    def save(self, commit=True):
        avis = super().save(commit=False)
        avis.user = self.user
        avis.structure = self.structure
        avis.plat = self.plat
        
        if commit:
            avis.save()
        return avis
