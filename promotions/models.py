from django.db import models
from plats.models import Plats

class Promotion(models.Model):
    plats = models.ForeignKey(Plats, on_delete=models.CASCADE, related_name='promotions')
    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    reduction = models.DecimalField(max_digits=5, decimal_places=2)  # Pourcentage ou montant fixe
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    def est_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.date_debut <= now <= self.date_fin

    def __str__(self):
        return f"{self.titre} - {self.plats.nom}"