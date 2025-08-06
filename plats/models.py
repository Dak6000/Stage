from django.conf import settings
from django.db import models

# Create your models here.

class Plats(models.Model):
    CATEGORIES = (
        ('entree', 'Entrée'),
        ('plat', 'Plat principal'),
        ('dessert', 'Dessert'),
        ('boisson', 'Boisson'),
    )

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    disponibilite = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='plats/', null=True, blank=True)
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Créateur")
    #createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom