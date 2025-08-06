from django.db import models

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

    note = models.IntegerField(choices=NOTE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avis')
    commentaire = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    signale = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_publication']

    def __str__(self):
        return f"Avis de {self.user} - Note: {self.note}"