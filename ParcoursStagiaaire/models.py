from django.db import models
from Employe.models import CLEmploye
from OrganizationalUnit.models import OrganizationalUnit
from Stagiaire.models import CLStagiaire

class CLParcoursStagiaire(models.Model):
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)
    stagiaire = models.ForeignKey(CLStagiaire, on_delete=models.CASCADE)
    responsable = models.ForeignKey(
        CLEmploye,
        on_delete=models.SET_NULL,
        related_name='parcours_responsable',
        null=True,
        blank=True,
    )
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    evaluation = models.CharField(max_length=255, blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    
    # Champ texte pour les compétences
    competences = models.TextField(
        blank=True,
        null=True,
        help_text="Entrez les compétences séparées par des virgules"
    )

    def __str__(self):
        return f"{self.stagiaire} - {self.organizational_unit}"
