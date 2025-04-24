from django.db import models

class Unite(models.Model):
    designation = models.CharField(max_length=50, unique=True)
    
    # Relation réflexive pour l'unité parente
    unite_parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sous_unites'
    )

    def __str__(self):
        if self.unite_parent:
            return f"{self.designation} (sous {self.unite_parent.designation})"
        return self.designation
