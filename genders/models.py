from uuid import uuid4, UUID
from django.db import models
from django.utils import timezone


class Gender(models.Model):
    class Meta:
        default_related_name = "genders"
        indexes = [
            models.Index(fields=["id", "name"])
        ]
        ordering = ["name"]
        verbose_name = "gender"
        verbose_name_plural = "genders"
    id = models.UUIDField(default=uuid4, primary_key=True,
                          editable=False, unique=True)
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
