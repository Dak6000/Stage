from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Avg
from accounts.models import User

# Create your models here.
class Avis(models.Model):
    NOTE_CHOICES = [
        (1, '1 - Très mauvais'),
        (2, '2 - Mauvais'),
        (3, '3 - Moyen'),
        (4, '4 - Bon'),
        (5, '5 - Excellent'),
    ]

    TYPE_AVIS_CHOICES = [
        ('structure', 'Structure'),
        ('plat', 'Plat'),
    ]

    note = models.IntegerField(
        choices=NOTE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avis')
    commentaire = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    signale = models.BooleanField(default=False)
    
    # Champs pour lier l'avis à une structure ou un plat
    type_avis = models.CharField(max_length=20, choices=TYPE_AVIS_CHOICES, null=True, blank=True)
    structure = models.ForeignKey(
        'structures.Structures', 
        on_delete=models.CASCADE, 
        related_name='avis_structure',
        null=True, 
        blank=True
    )
    plat = models.ForeignKey(
        'plats.Plats', 
        on_delete=models.CASCADE, 
        related_name='avis_plat',
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['-date_publication']
        unique_together = ['user', 'structure', 'plat']  # Un seul avis par utilisateur par structure/plat

    def __str__(self):
        if self.structure:
            return f"Avis de {self.user} sur {self.structure.nom} - Note: {self.note}"
        elif self.plat:
            return f"Avis de {self.user} sur {self.plat.nom} - Note: {self.note}"
        return f"Avis de {self.user} - Note: {self.note}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Vérifier qu'un seul objet est lié (structure OU plat)
        if self.structure and self.plat:
            raise ValidationError("Un avis ne peut être lié qu'à une structure OU un plat, pas les deux.")
        if not self.structure and not self.plat:
            raise ValidationError("Un avis doit être lié à une structure ou un plat.")
        
        # Définir le type d'avis automatiquement
        if self.structure:
            self.type_avis = 'structure'
        elif self.plat:
            self.type_avis = 'plat'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
        # Mettre à jour la note moyenne de la structure ou du plat
        if self.structure:
            self.update_structure_rating()
        elif self.plat:
            self.update_plat_rating()

    def update_structure_rating(self):
        """Met à jour la note moyenne de la structure"""
        from structures.models import Structures
        avis_structure = Avis.objects.filter(structure=self.structure, signale=False)
        if avis_structure.exists():
            note_moyenne = avis_structure.aggregate(Avg('note'))['note__avg']
            nombre_avis = avis_structure.count()
            
            # Mettre à jour la structure
            self.structure.note_moyenne = round(note_moyenne, 2)
            self.structure.nombre_avis = nombre_avis
            self.structure.save()

    def update_plat_rating(self):
        """Met à jour la note moyenne du plat"""
        from plats.models import Plats
        avis_plat = Avis.objects.filter(plat=self.plat, signale=False)
        if avis_plat.exists():
            note_moyenne = avis_plat.aggregate(Avg('note'))['note__avg']
            nombre_avis = avis_plat.count()
            
            # Mettre à jour le plat
            self.plat.note_moyenne = round(note_moyenne, 2)
            self.plat.nombre_avis = nombre_avis
            self.plat.save()

    def get_note_etoiles(self):
        """Retourne le nombre d'étoiles pour l'affichage"""
        return self.note

    def get_note_display(self):
        """Retourne la note formatée pour l'affichage"""
        return f"{self.note}/5"

    def get_date_relative(self):
        """Retourne la date relative (ex: 'il y a 2 jours')"""
        from django.utils import timezone
        now = timezone.now()
        diff = now - self.date_publication
        
        if diff.days == 0:
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
            else:
                hours = diff.seconds // 3600
                return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        elif diff.days == 1:
            return "hier"
        elif diff.days < 7:
            return f"il y a {diff.days} jour{'s' if diff.days > 1 else ''}"
        else:
            return self.date_publication.strftime("%d/%m/%Y")