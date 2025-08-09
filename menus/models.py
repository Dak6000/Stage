from django.conf import settings
from django.db import models
from django.utils import timezone

from structures.models import Structures


# Create your models here.
class Menus(models.Model):
    STATUS_CHOICES = (
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('brouillon', 'Brouillon'),
    )

    nom = models.CharField(max_length=100)
    date_creation = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='brouillon')
    # Un plat ne doit appartenir qu'à un seul menu.
    # On retire le ManyToMany et on gère la relation inverse sur Plats via ForeignKey
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Créateur")
    structure = models.ForeignKey(Structures, on_delete=models.CASCADE, related_name='menus')

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return self.nom

    def clean(self):
        # Cohérence: le créateur du menu doit posséder la structure
        if self.createur_id and self.structure_id:
            if self.structure.user_id != self.createur_id:
                from django.core.exceptions import ValidationError
                raise ValidationError("Le menu doit appartenir à une structure du même utilisateur.")
