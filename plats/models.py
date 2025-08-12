from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from structures.models import Structures
from datetime import datetime, time as dt_time

# Create your models here.

class Plats(models.Model):
    CATEGORIES = (
        ('entree', 'Entrée'),
        ('plat', 'Plat principal'),
        ('dessert', 'Dessert'),
        ('boisson', 'Boisson'),
        ('glass', 'Glass'),
        ('africain', 'Africain'),
    )

    DIFFICULTE_CHOICES = (
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    )

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    disponibilite = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='plats/', null=True, blank=True)
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Créateur")
    structure = models.ForeignKey(Structures, on_delete=models.CASCADE, related_name='plats', null=True, blank=True)
    
    # Nouveaux champs
    temps_preparation = models.IntegerField(help_text="Temps de préparation en minutes", default=30)
    ingredients = models.TextField(blank=True, help_text="Liste des ingrédients")
    allergenes = models.CharField(max_length=200, blank=True, help_text="Allergènes présents")
    calories = models.IntegerField(blank=True, null=True, help_text="Calories par portion")
    portion = models.CharField(max_length=50, blank=True, help_text="Taille de la portion")
    difficulte = models.CharField(max_length=20, choices=DIFFICULTE_CHOICES, default='moyen')
    temps_cuisson = models.IntegerField(blank=True, null=True, help_text="Temps de cuisson en minutes")
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    nombre_avis = models.IntegerField(default=0)
    
    # Champs pour les promotions
    en_promotion = models.BooleanField(default=False, verbose_name="En promotion")
    prix_promotionnel = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Prix promotionnel")
    date_debut_promotion = models.DateTimeField(null=True, blank=True)
    heure_debut_promotion = models.CharField(max_length=100, blank=True, null=True)
    heure_fin_promotion = models.CharField(max_length=100, blank=True, null=True)
    date_fin_promotion = models.DateTimeField(null=True, blank=True)
    pourcentage_reduction = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Pourcentage de réduction")
    description_promotion = models.TextField(blank=True, verbose_name="Description de la promotion")

    class Meta:
        ordering = ['nom']
        verbose_name = "Plat"
        verbose_name_plural = "Plats"

    def __str__(self):
        return self.nom

    def clean(self):
        # S'assurer que le plat est rattaché à la structure du créateur s'il en a une
        # et empêcher une incohérence createur/structure
        if self.createur_id:
            # Récupère éventuellement la structure de l'utilisateur
            user_structure = getattr(self.createur, 'structure', None)
            if user_structure is not None:
                user_structure = user_structure.first()
            # Si une structure est définie côté plat, elle doit correspondre à celle de l'utilisateur
            if self.structure_id and user_structure and self.structure_id != user_structure.id:
                raise ValidationError("La structure du plat doit correspondre à la structure du créateur.")
        
        # Validation des dates de promotion
        if self.en_promotion:
            if self.date_debut_promotion and self.date_fin_promotion:
                if self.date_fin_promotion < self.date_debut_promotion:
                    raise ValidationError("La date de fin de promotion doit être postérieure à la date de début.")
            
            # Validation du format des heures si elles sont renseignées
            if self.heure_debut_promotion:
                try:
                    datetime.strptime(self.heure_debut_promotion, '%H:%M')
                except ValueError:
                    raise ValidationError("Format d'heure de début invalide. Utilisez HH:MM.")
            
            if self.heure_fin_promotion:
                try:
                    datetime.strptime(self.heure_fin_promotion, '%H:%M')
                except ValueError:
                    raise ValidationError("Format d'heure de fin invalide. Utilisez HH:MM.")
        
        return super().clean()

    def get_prix_affichage(self):
        """Retourne le prix formaté pour l'affichage"""
        if self.est_en_promotion():
            return f"{self.get_prix_promotionnel()} FCFA"
        return f"{self.prix} FCFA"

    def get_temps_total(self):
        """Retourne le temps total (préparation + cuisson)"""
        temps_cuisson = self.temps_cuisson or 0
        return self.temps_preparation + temps_cuisson

    def get_note_etoiles(self):
        """Retourne le nombre d'étoiles pour l'affichage"""
        return round(self.note_moyenne)

    def get_note_display(self):
        """Retourne la note formatée pour l'affichage"""
        return f"{self.note_moyenne}/5"

    def get_categorie_display(self):
        """Retourne le nom de la catégorie"""
        return dict(self.CATEGORIES)[self.categorie]
    
    def est_en_promotion(self):
        """Vérifie si le plat est actuellement en promotion"""
        if not self.en_promotion:
            return False
        
        now = timezone.now()
        
        # Si aucune date n'est définie, la promotion est toujours active
        if not self.date_debut_promotion and not self.date_fin_promotion:
            return True
        
        try:
            # Gestion de la date/heure de début
            debut_promo = None
            if self.date_debut_promotion:
                heure_debut = (datetime.strptime(self.heure_debut_promotion, '%H:%M').time() 
                            if self.heure_debut_promotion else dt_time.min)
                debut_promo = timezone.make_aware(
                    datetime.combine(self.date_debut_promotion, heure_debut)
                )
            
            # Gestion de la date/heure de fin
            fin_promo = None
            if self.date_fin_promotion:
                heure_fin = (datetime.strptime(self.heure_fin_promotion, '%H:%M').time()
                            if self.heure_fin_promotion else dt_time.max)
                fin_promo = timezone.make_aware(
                    datetime.combine(self.date_fin_promotion, heure_fin)
                )
            
            # Vérification de la période de promotion
            if debut_promo and fin_promo:
                return debut_promo <= now <= fin_promo
            elif debut_promo:
                return now >= debut_promo
            elif fin_promo:
                return now <= fin_promo
            return True
                
        except (ValueError, TypeError, AttributeError):
            # En cas d'erreur (format d'heure invalide, etc.)
            return False
    
    def get_prix_promotionnel(self):
        """Retourne le prix promotionnel calculé"""
        if not self.est_en_promotion():
            return self.prix
        
        if self.prix_promotionnel:
            return self.prix_promotionnel
        
        if self.pourcentage_reduction:
            reduction = self.prix * (self.pourcentage_reduction / 100)
            return max(self.prix - reduction, 0)
        
        return self.prix
    
    def get_economie(self):
        """Calcule le montant économisé"""
        if not self.est_en_promotion():
            return 0
        
        prix_promo = self.get_prix_promotionnel()
        return self.prix - prix_promo
    
    def get_pourcentage_economie(self):
        """Calcule le pourcentage d'économie"""
        if not self.est_en_promotion() or self.prix == 0:
            return 0
        
        economie = self.get_economie()
        return (economie / self.prix) * 100
    
    def get_jours_restants_promotion(self):
        """Calcule le nombre de jours restants pour la promotion"""
        if not self.est_en_promotion() or not self.date_fin_promotion:
            return 0
        
        now = timezone.now()
        if self.date_fin_promotion > now:
            delta = self.date_fin_promotion - now
            return delta.days
        return 0