from datetime import datetime  # Ajoutez cette ligne en haut du fichier
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.forms.widgets import SplitDateTimeWidget

from plats.models import Plats

User = get_user_model()

class PromotionForm(forms.ModelForm):
    """Formulaire dédié à la gestion des promotions"""
    
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
    
    date_heure_debut_promotion = forms.SplitDateTimeField(
        required=False,
        widget=SplitDateTimeWidget(
            date_attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'date_debut_promotion',
                'min': timezone.now().strftime('%Y-%m-%d')
            },
            time_attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'heure_debut_promotion'
            },
            date_format='%Y-%m-%d',
            time_format='%H:%M'
        ),
        help_text="Date et heure de début de la promotion",
        error_messages={
            'invalid': "Format de date/heure invalide."
        }
    )

    date_heure_fin_promotion = forms.SplitDateTimeField(
        required=False,
        widget=SplitDateTimeWidget(
            date_attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'date_fin_promotion',
                'min': timezone.now().strftime('%Y-%m-%d')
            },
            time_attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'heure_fin_promotion'
            },
            date_format='%Y-%m-%d',
            time_format='%H:%M'
        ),
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
            'prix_promotionnel', 'date_heure_debut_promotion',
            'date_heure_fin_promotion', 'pourcentage_reduction', 'description_promotion'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si l'instance existe, initialise les champs combinés
        if self.instance and self.instance.pk:
            if self.instance.date_debut_promotion and self.instance.heure_debut_promotion:
                try:
                    self.initial['date_heure_debut_promotion'] = timezone.make_aware(
                        datetime.combine(
                            self.instance.date_debut_promotion,
                            datetime.strptime(self.instance.heure_debut_promotion, '%H:%M').time()
                        )
                    )
                except (ValueError, TypeError):
                    pass
            
            if self.instance.date_fin_promotion and self.instance.heure_fin_promotion:
                try:
                    self.initial['date_heure_fin_promotion'] = timezone.make_aware(
                        datetime.combine(
                            self.instance.date_fin_promotion,
                            datetime.strptime(self.instance.heure_fin_promotion, '%H:%M').time()
                        )
                    )
                except (ValueError, TypeError):
                    pass

    def clean(self):
        cleaned_data = super().clean()
        prix_promotionnel = cleaned_data.get('prix_promotionnel')
        pourcentage_reduction = cleaned_data.get('pourcentage_reduction')
        date_heure_debut = cleaned_data.get('date_heure_debut_promotion')
        date_heure_fin = cleaned_data.get('date_heure_fin_promotion')
        prix = self.instance.prix if self.instance else 0

        # Logique simplifiée : dès qu'une information promotionnelle est fournie, on active la promotion
        
        # Calcul automatique prix ↔ pourcentage
        if prix_promotionnel and not pourcentage_reduction:
            # Si prix promotionnel fourni, calculer le pourcentage
            if prix > 0:
                reduction = prix - prix_promotionnel
                pourcentage_calcule = (reduction / prix) * 100
                cleaned_data['pourcentage_reduction'] = round(pourcentage_calcule, 2)
        
        elif pourcentage_reduction and not prix_promotionnel:
            # Si pourcentage fourni, calculer le prix promotionnel
            if pourcentage_reduction > 0 and pourcentage_reduction < 100:
                reduction = prix * (pourcentage_reduction / 100)
                prix_calcule = prix - reduction
                cleaned_data['prix_promotionnel'] = round(prix_calcule, 2)
        
        elif prix_promotionnel and pourcentage_reduction:
            # Si les deux sont fournis, priorité au prix promotionnel
            if prix > 0:
                reduction = prix - prix_promotionnel
                pourcentage_calcule = (reduction / prix) * 100
                cleaned_data['pourcentage_reduction'] = round(pourcentage_calcule, 2)
        
        # Validation minimale des dates (optionnel)
        if date_heure_debut and date_heure_fin:
            if date_heure_debut >= date_heure_fin:
                raise ValidationError("La date/heure de fin doit être postérieure à la date/heure de début.")
        
        # Sauvegarde des composants date et heure séparément pour le modèle
        if date_heure_debut:
            cleaned_data['date_debut_promotion'] = date_heure_debut.date()
            cleaned_data['heure_debut_promotion'] = date_heure_debut.time().strftime('%H:%M')
        if date_heure_fin:
            cleaned_data['date_fin_promotion'] = date_heure_fin.date()
            cleaned_data['heure_fin_promotion'] = date_heure_fin.time().strftime('%H:%M')

        return cleaned_data
    
    def save(self, commit=True):
        # Sauvegarde d'abord l'instance de base
        plat = super().save(commit=False)
        
        # Récupère les données nettoyées
        cleaned_data = self.cleaned_data
        
        # Activer la promotion dès qu'une information promotionnelle est fournie
        has_promo_info = (
            cleaned_data.get('prix_promotionnel') or 
            cleaned_data.get('pourcentage_reduction') or 
            cleaned_data.get('description_promotion') or
            cleaned_data.get('date_debut_promotion') or
            cleaned_data.get('date_fin_promotion')
        )
        
        if has_promo_info:
            plat.en_promotion = True
        
        # Gestion des champs de promotion
        plat.prix_promotionnel = cleaned_data.get('prix_promotionnel')
        plat.pourcentage_reduction = cleaned_data.get('pourcentage_reduction')
        plat.description_promotion = cleaned_data.get('description_promotion', '')
        
        # Gestion des dates/heures de promotion
        plat.date_debut_promotion = cleaned_data.get('date_debut_promotion')
        plat.heure_debut_promotion = cleaned_data.get('heure_debut_promotion')
        plat.date_fin_promotion = cleaned_data.get('date_fin_promotion')
        plat.heure_fin_promotion = cleaned_data.get('heure_fin_promotion')
        
        # Sauvegarde si commit=True
        if commit:
            plat.save()
            self.save_m2m()  # Important pour les relations many-to-many si vous en avez
        
        return plat

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

    class Meta:
        model = Plats
        fields = [
            'nom', 'description', 'prix', 'categorie', 'disponibilite', 'photo',
            'temps_preparation', 'temps_cuisson', 'ingredients', 'allergenes',
            'calories', 'portion', 'difficulte'
        ]

    def clean(self):
        cleaned_data = super().clean()

        # Validation du temps total
        temps_preparation = cleaned_data.get('temps_preparation', 0) or 0
        temps_cuisson = cleaned_data.get('temps_cuisson', 0) or 0
        temps_total = temps_preparation + temps_cuisson

        if temps_total > 1440:  # 24h en minutes
            raise ValidationError("Le temps total (préparation + cuisson) ne peut excéder 24h (1440 minutes).")

        return cleaned_data
    
    def save(self, commit=True):
        # Sauvegarde d'abord l'instance de base
        plat = super().save(commit=False)
        
        # Sauvegarde si commit=True
        if commit:
            plat.save()
            self.save_m2m()  # Important pour les relations many-to-many si vous en avez
        
        return plat
