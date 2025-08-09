from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    # Relation ManyToMany avec les plats (un plat peut appartenir à 0..n menus)
    plats = models.ManyToManyField('plats.Plats', through='MenuPlat', related_name='menus', blank=True)
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
                raise ValidationError("Le menu doit appartenir à une structure du même utilisateur.")


class MenuPlat(models.Model):
    menu = models.ForeignKey('menus.Menus', on_delete=models.CASCADE)
    plat = models.ForeignKey('plats.Plats', on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('menu', 'plat')
        verbose_name = 'Association menu-plat'
        verbose_name_plural = 'Associations menu-plats'

    def clean(self):
        # Un plat ne peut être associé qu'à un menu créé par le même utilisateur
        if self.menu_id and self.plat_id:
            if self.menu.createur_id != self.plat.createur_id:
                raise ValidationError("Le plat doit appartenir à un menu créé par le même utilisateur.")
            # Vérifier que la structure du plat correspond à celle du menu (empêche le cross-structure)
            if self.plat.structure_id and self.menu.structure_id and self.plat.structure_id != self.menu.structure_id:
                raise ValidationError("Un plat ne peut pas être associé à un menu d'une autre structure.")

    def __str__(self):
        return f"{self.menu} ↔ {self.plat}"
