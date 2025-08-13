from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import User


# Create your models here.

class Structures(models.Model):

    TYPE_CHOICES = (
        ('restaurant', 'Restaurant'),
        ('fastfood', 'Fast Food'),
        ('cafe', 'Café'),
        ('boulangerie', 'Boulangerie'),
        ('traiteur', 'Traiteur'),
        ('autre', 'Autre'),
    )

    VILLE_CHOICES = (
        ('Lomé', 'Lomé'),
        ('Kara', 'Kara'),
        ('Sokodé', 'Sokodé'),
        ('Atakpamé', 'Atakpamé'),
        ('Tsévié', 'Tsévié'),
        ('Aného', 'Aného'),
        ('Mango', 'Mango'),
        ('Dapaong', 'Dapaong'),
        ('Autre', 'Autre'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='structure')
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100, choices=VILLE_CHOICES)
    heure_ouverture = models.CharField(max_length=100, blank=True, null=True)
    heure_fermeture = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    photo = models.ImageField(upload_to='structures/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    featured = models.BooleanField(default=False, verbose_name="Mettre en avant")
    
    # Champs pour les notes et avis
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name="Note moyenne")
    nombre_avis = models.IntegerField(default=0, verbose_name="Nombre d'avis")

    class Meta:
        ordering = ['-date_creation']
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_structure_per_user'),
        ]

    def __str__(self):
        return self.nom

    def clean(self):
        # Limiter à 1 structure par utilisateur
        if self.user_id:
            qs = Structures.objects.filter(user_id=self.user_id)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Chaque utilisateur ne peut posséder qu'une seule structure.")

    def get_note_etoiles(self):
        """Retourne le nombre d'étoiles pour l'affichage"""
        return round(self.note_moyenne)

    def get_note_display(self):
        """Retourne la note formatée pour l'affichage"""
        return f"{self.note_moyenne}/5"

    def get_avis_count(self):
        """Retourne le nombre d'avis"""
        return self.avis_structure.count()

    def get_avis_recent(self, limit=5):
        """Retourne les avis les plus récents"""
        return self.avis_structure.filter(signale=False).order_by('-date_publication')[:limit]
