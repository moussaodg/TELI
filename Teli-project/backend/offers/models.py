from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from accounts.models import Administrator

class BaseOffer(models.Model):
    specification = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

class DailyOffer(BaseOffer):
    day = models.DateField(unique=True)

    def __str__(self):
        return f"Offre du jour : {self.specification} - {self.day:%d/%m/%Y}"

class SpecialOffer(BaseOffer):
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")

    def __str__(self):
        return f"Offre spéciale : {self.specification} ({self.start_date:%d/%m/%Y} - {self.end_date:%d/%m/%Y})"

class Offer(models.Model):
    code = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Utilisation du modèle utilisateur configuré dans settings
    configurator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    daily_offer = models.ForeignKey(DailyOffer, on_delete=models.SET_NULL, null=True, blank=True)
    special_offer = models.ForeignKey(SpecialOffer, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        # Empêcher le double type d'offre
        if self.daily_offer and self.special_offer:
            raise ValidationError("Une offre ne peut pas être à la fois journalière et spéciale.")

    def sync_rasa(self):
        # Placeholder for offer synchronization with Rasa / chatbot backend.
        # This should be extended with the actual integration point.
        return True

    def __str__(self):
        return f"Offre {self.code} - {self.price}FCFA - Configurateur: {self.configurator.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_rasa()