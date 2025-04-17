from django.db import models
from Employe.models import CLEmploye
from OrganizationalUnit.models import OrganizationalUnit
from Stagiaire.models import CLStagiaire  # Assurez-vous que le chemin est correct

class CLParcoursStagiaire(models.Model):
    # Clés étrangères vers les autres modèles
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)
    stagiaire = models.ForeignKey(CLStagiaire, on_delete=models.CASCADE)
    responsable = models.ForeignKey(
        CLEmploye,
        on_delete=models.SET_NULL,
         related_name='parcours_responsable',  # Nouveau nom pour éviter le conflit
        null=True,
        blank=True,
    )
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    # Nouveaux champs ajoutés
    evaluation = models.CharField(max_length=255, blank=True, null=True, help_text="Évaluation du stagiaire")
    commentaire = models.TextField(blank=True, null=True, help_text="Commentaires sur le stagiaire")
    competence = models.CharField(max_length=255, blank=True, null=True, help_text="Compétence évaluée du stagiaire")

    def __str__(self):
        return f"{self.stagiaire} - {self.responsable} à {self.organizational_unit}"
