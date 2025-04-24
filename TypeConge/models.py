from django.db import models
from calendar import monthrange

class CLTypeConge(models.Model):
    MOIS_CHOICES = [
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre'),
    ]

    designation = models.CharField(max_length=50, unique=True)
    periode_conge = models.IntegerField(help_text="Durée du congé en jours")
    mois_debut_autorise = models.IntegerField(
        choices=MOIS_CHOICES,
        help_text="Mois de début autorisé pour ce type de congé"
    )

    def __str__(self):
        mois_nom = dict(self.MOIS_CHOICES).get(self.mois_debut_autorise, "Inconnu")
        return f"{self.designation} ({self.periode_conge} jours) - Début autorisé en {mois_nom}"

    def calculer_mois_fin(self):
        """Calculer le mois de fin du congé basé sur le mois de début et la durée"""
        mois_debut = self.mois_debut_autorise
        jours_dans_mois = monthrange(2022, mois_debut)[1]  # Année fictive pour obtenir les jours du mois
        total_jours = self.periode_conge
        mois_fin = mois_debut
        while total_jours > jours_dans_mois:
            total_jours -= jours_dans_mois
            mois_fin += 1
            if mois_fin > 12:
                mois_fin = 1
        return mois_fin
