from django.db import models
from users.models import ClUser
from  specialite.models import  Specialite    # Assure-toi que ce chemin est correct selon l'organisation de ton projet

# Modèle employé avec spécialité
class CLEmploye(ClUser):
    specialite = models.ForeignKey(
        Specialite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employes'
    )

    def save(self, *args, **kwargs):
        self.tstt = "Employé (e)"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tnm} {self.tpm} - Employé (e)"
