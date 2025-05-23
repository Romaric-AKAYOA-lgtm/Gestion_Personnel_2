from django.db import models
from unite.models import Unite  # Veille à ce que le modèle Unite soit bien défini

class OrganizationalUnit(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nom de l'unité (ex. 'II-1-1 Sections Français')"
    )
    designation = models.TextField(
        blank=True,
        null=True,
        help_text="Désignation ou description de l'unité"
    )
    unite = models.ForeignKey(
        Unite,
        on_delete=models.CASCADE,
        related_name="organizational_units",
        help_text="Unité de rattachement (par exemple, une unité fonctionnelle globale)"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_units',
        help_text="Unité parente dans la hiérarchie (laisser vide pour une unité de premier niveau)"
    )

    class Meta:
        verbose_name = "Unité Organisationnelle"
        verbose_name_plural = "Unités Organisationnelles"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_full_hierarchy(self):
        """
        Retourne la hiérarchie complète de l'unité sous forme de chaîne.
        Exemple : "Service A > Division B > Section C"
        """
        if self.parent:
            return f"{self.parent.get_full_hierarchy()} > {self.name}"
        return self.name
