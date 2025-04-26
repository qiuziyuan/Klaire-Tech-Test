from django.db import models

class Address(models.Model):
    """Stocke les informations d'une adresse obtenue via une API externe."""
    label = models.CharField(max_length=255)
    housenumber = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=20)
    citycode = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ('latitude', 'longitude')  # Garantir l'unicité latitude/longitude

    def __str__(self):
        return self.label