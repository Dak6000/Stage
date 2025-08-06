from django.db import models

from accounts.models import User


# Create your models here.

class Structures(models.Model):
    TYPE_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Café'),
        ('bar', 'Bar'),
        ('hotel', 'Hôtel'),
        ('autre', 'Autre'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='structure')
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    heure_ouverture = models.CharField(max_length=100, blank=True, null=True)
    heure_fermeture = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    photo = models.ImageField(upload_to='structures/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    featured = models.BooleanField(default=False, verbose_name="Mettre en avant")

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return self.nom
