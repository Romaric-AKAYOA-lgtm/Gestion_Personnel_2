from django.db import models
from users.models import ClUser
from OrganizationalUnit.models import OrganizationalUnit
# Modèle Stagiaire avec spécialité
class CLStagiaire(ClUser):
    # Ajouter les nouveaux champs
    etablissement = models.CharField(max_length=100, blank=True, null=True, help_text="Nom de l'établissement")
    theme = models.CharField(max_length=200, blank=True, null=True, help_text="Thème du stage")
    filiere = models.CharField(max_length=100, blank=True, null=True, help_text="Filière du stagiaire")
    option = models.CharField(max_length=100, blank=True, null=True, help_text="Option du stagiaire")
    date_debut = models.DateField(null=True, blank=True, help_text="Date de début du stage")
    date_fin = models.DateField(null=True, blank=True, help_text="Date de fin du stage")

    # Ajouter la clé étrangère pour le responsable (clé étrangère vers ClUser)
    responsable = models.ForeignKey(ClUser, on_delete=models.CASCADE, related_name='responsables', null=True, blank=True, help_text="Responsable du stagiaire")

    # Ajouter la clé étrangère pour l'unité organisationnelle
    organisationUnit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, related_name='stagiaires', null=True, blank=True, help_text="Unité organisationnelle du stagiaire")

    def save(self, *args, **kwargs):
        # Définir 'tstt' comme 'Stagiaire' au lieu de 'Employé (e)'
        self.tstt = "Stagiaire"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tnm} {self.tpm} - Stagiaire"
