from django.conf import settings
from django.db import models
from django.utils import timezone

from plats.models import Plats  # Assurez-vous que ce chemin d'importation est correct
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
    plats = models.ManyToManyField(Plats, related_name='menus')
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Créateur")
    #createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structures, on_delete=models.CASCADE, related_name='menus')

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return self.nom

class MenuPlat(models.Model):
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE)
    plats = models.ForeignKey(Plats, on_delete=models.CASCADE)  # Référence correcte