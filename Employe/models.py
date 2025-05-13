from users.models import ClUser

# Modèle employé sans spécialité
class CLEmploye(ClUser):
    def save(self, *args, **kwargs):
        self.tstt = "Employé (e)"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tnm} {self.tpm} "
