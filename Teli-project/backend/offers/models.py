from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Offer(models.Model):
    code = models.CharField(max_length=20, unique=True)
    specification = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    configurator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def sync_rasa(self):
        # Placeholder for offer synchronization with Rasa / chatbot backend.
        # This should be extended with the actual integration point.
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_rasa()

    def __str__(self):
        return f"Offre {self.code} - {self.price}FCFA - Configurateur: {self.configurator.username}"

class DailyOffer(Offer):
    day = models.DateField(unique=True)

    def clean(self):
        if DailyOffer.objects.exclude(pk=self.pk).filter(code=self.code).exists() or SpecialOffer.objects.exclude(pk=self.pk).filter(code=self.code).exists():
            raise ValidationError("Le code d'offre doit être unique entre toutes les offres.")

    def __str__(self):
        return f"Offre du jour : {self.specification} - {self.day:%d/%m/%Y}"

class SpecialOffer(Offer):
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")

        if DailyOffer.objects.exclude(pk=self.pk).filter(code=self.code).exists() or SpecialOffer.objects.exclude(pk=self.pk).filter(code=self.code).exists():
            raise ValidationError("Le code d'offre doit être unique entre toutes les offres.")

    def __str__(self):
        return f"Offre spéciale : {self.specification} ({self.start_date:%d/%m/%Y} - {self.end_date:%d/%m/%Y})"