from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

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
            'step': '0.01',
            'min': '100'
        }),
        help_text="Prix minimum: 100 Fcfa",
        error_messages={
            'min_value': "Le prix minimum est de 100 Fcfa.",
            'max_value': "Le prix maximum est de 1 000 000 Fcfa."
        }
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
    
    # Nouveaux champs
    temps_preparation = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Temps en minutes',
            'min': '1'
        }),
        help_text="Temps de préparation en minutes",
        error_messages={
            'min_value': "Le temps minimum est de 1 minute.",
            'max_value': "Le temps maximum est de 1440 minutes (24h)."
        }
    )
    temps_cuisson = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Temps en minutes (optionnel)',
            'min': '0',
            'max': '1440'
        }),
        help_text="Temps de cuisson en minutes (0-1440)",
        error_messages={
            'min_value': "Le temps ne peut pas être négatif.",
            'max_value': "Le temps maximum est de 1440 minutes (24h)."
        }
    )
    ingredients = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Liste des ingrédients (un par ligne)'
        }),
        help_text="Liste des ingrédients nécessaires"
    )
    allergenes = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Gluten, Lactose, Fruits à coque...'
        }),
        help_text="Allergènes présents dans le plat"
    )
    calories = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calories par portion',
            'min': '0'
        }),
        help_text="Calories par portion (optionnel)"
    )
    portion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 1 assiette, 200g...'
        }),
        help_text="Taille de la portion"
    )
    difficulte = forms.ChoiceField(
        choices=Plats.DIFFICULTE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Niveau de difficulté de préparation"
    )
    
    # Champs pour les promotions
    en_promotion = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'en_promotion'
        }),
        help_text="Activer la promotion pour ce plat"
    )
    prix_promotionnel = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix promotionnel (en Fcfa)',
            'step': '0.01',
            'id': 'prix_promotionnel'
        }),
        help_text="Prix promotionnel (laissez vide pour utiliser le pourcentage de réduction)"
    )
    date_debut_promotion = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'id': 'date_debut_promotion',
            'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
        }),
        help_text="Date et heure de début de la promotion",
        error_messages={
            'invalid': "Format de date/heure invalide."
        }
    )

    date_fin_promotion = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'id': 'date_fin_promotion',
            'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
        }),
        help_text="Date et heure de fin de la promotion",
        error_messages={
            'invalid': "Format de date/heure invalide."
        }
    )
    pourcentage_reduction = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pourcentage de réduction',
            'step': '0.01',
            'min': '0',
            'max': '100',
            'id': 'pourcentage_reduction'
        }),
        help_text="Pourcentage de réduction (utilisé si le prix promotionnel n'est pas défini)"
    )
    description_promotion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Description de la promotion (optionnel)',
            'id': 'description_promotion'
        }),
        help_text="Description de la promotion"
    )

    class Meta:
        model = Plats
        fields = [
            'nom', 'description', 'prix', 'categorie', 'disponibilite', 'photo',
            'temps_preparation', 'temps_cuisson', 'ingredients', 'allergenes',
            'calories', 'portion', 'difficulte',
            'en_promotion', 'prix_promotionnel', 'date_debut_promotion', 
            'date_fin_promotion', 'pourcentage_reduction', 'description_promotion'
        ]

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix < 100:
            raise ValidationError("Le prix minimum est de 100 Fcfa.")
        if prix > 1000000:
            raise ValidationError("Le prix maximum est de 1 000 000 Fcfa.")
        return prix

    def clean_temps_preparation(self):
        temps = self.cleaned_data.get('temps_preparation')
        if temps < 1:
            raise ValidationError("Le temps de préparation doit être d'au moins 1 minute.")
        if temps > 1440:  # 24h en minutes
            raise ValidationError("Le temps de préparation ne peut excéder 24h (1440 minutes).")
        return temps

    def clean_temps_cuisson(self):
        temps = self.cleaned_data.get('temps_cuisson')
        if temps is not None:
            if temps < 0:
                raise ValidationError("Le temps de cuisson ne peut pas être négatif.")
            if temps > 1440:
                raise ValidationError("Le temps de cuisson ne peut excéder 24h (1440 minutes).")
        return temps

    def clean_calories(self):
        calories = self.cleaned_data.get('calories')
        if calories is not None and calories < 0:
            raise ValidationError("Les calories ne peuvent pas être négatives.")
        return calories

    def clean_pourcentage_reduction(self):
        reduction = self.cleaned_data.get('pourcentage_reduction')
        if reduction is not None:
            if reduction <= 0 or reduction >= 100:
                raise ValidationError("Le pourcentage de réduction doit être entre 0 et 100%.")
        return reduction

    def clean(self):
        cleaned_data = super().clean()
        en_promotion = cleaned_data.get('en_promotion')
        prix_promotionnel = cleaned_data.get('prix_promotionnel')
        pourcentage_reduction = cleaned_data.get('pourcentage_reduction')
        date_debut_promotion = cleaned_data.get('date_debut_promotion')
        date_fin_promotion = cleaned_data.get('date_fin_promotion')
        prix = cleaned_data.get('prix')
        now = timezone.now()

        # Validation des promotions
        if en_promotion:
            # Vérification des champs promotionnels
            if prix_promotionnel and pourcentage_reduction:
                raise ValidationError("Vous devez spécifier soit un prix promotionnel, soit un pourcentage de réduction, mais pas les deux.")

            if not prix_promotionnel and not pourcentage_reduction:
                raise ValidationError("Vous devez spécifier soit un prix promotionnel soit un pourcentage de réduction.")

            if prix_promotionnel and prix_promotionnel >= prix:
                raise ValidationError("Le prix promotionnel doit être inférieur au prix original.")

            if pourcentage_reduction:
                if pourcentage_reduction <= 0 or pourcentage_reduction >= 100:
                    raise ValidationError("Le pourcentage de réduction doit être entre 0 et 100%.")
                # Calcul automatique du prix promotionnel si seulement le pourcentage est fourni
                cleaned_data['prix_promotionnel'] = prix - (prix * pourcentage_reduction / 100)

            # Validation complète des dates
            if date_debut_promotion or date_fin_promotion:
                # Si une seule date est renseignée
                if bool(date_debut_promotion) != bool(date_fin_promotion):
                    raise ValidationError("Vous devez spécifier à la fois la date de début et de fin de promotion.")
                
                # Si les deux dates sont renseignées
                if date_debut_promotion and date_fin_promotion:
                    if date_debut_promotion >= date_fin_promotion:
                        raise ValidationError("La date de fin doit être postérieure à la date de début.")
                    
                    if date_debut_promotion < now:
                        raise ValidationError("La date de début ne peut pas être dans le passé.")
                    
                    # Optionnel : vérifier que la promotion dure au moins 1 heure
                    if (date_fin_promotion - date_debut_promotion).total_seconds() < 3600:
                        raise ValidationError("La promotion doit durer au moins 1 heure.")
            else:
                # Si aucune date n'est renseignée, la promotion est considérée comme permanente
                pass

        # Si la promotion est désactivée, on nettoie les champs promotionnels
        if not en_promotion:
            cleaned_data['prix_promotionnel'] = None
            cleaned_data['pourcentage_reduction'] = None
            cleaned_data['date_debut_promotion'] = None
            cleaned_data['date_fin_promotion'] = None
            cleaned_data['description_promotion'] = ''

        # Validation du temps total
        temps_preparation = cleaned_data.get('temps_preparation', 0) or 0
        temps_cuisson = cleaned_data.get('temps_cuisson', 0) or 0
        temps_total = temps_preparation + temps_cuisson

        if temps_total > 1440:  # 24h en minutes
            raise ValidationError("Le temps total (préparation + cuisson) ne peut excéder 24h (1440 minutes).")

        return cleaned_data
