from django.db import models

class Fonction(models.Model):
    designation = models.CharField(max_length=50, unique=True)
    
    # Relation réflexive : une fonction peut avoir une fonction "parent"
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sous_fonctions'
    )

    def __str__(self):
        if self.parent:
            return f"{self.designation} (sous {self.parent.designation})"
        return self.designation
