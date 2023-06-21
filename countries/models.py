from uuid import uuid4, UUID
from django.db import models
from django.utils import timezone

class Country(models.Model):
    class Meta:
        default_related_name = "countries"
        indexes = [
            models.Index(fields=["id", "name"])
        ]
        ordering = ["name"]
        verbose_name = "country"
        verbose_name_plural = "countries"
    id = models.UUIDField(default=uuid4, primary_key=True,
                          editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=5, unique=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

