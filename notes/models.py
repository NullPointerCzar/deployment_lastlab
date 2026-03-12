from django.db import models
from django.core.exceptions import ValidationError


def validate_min_length(value):
    if len(value) < 10:
        raise ValidationError("Description must be at least 10 characters long.")


class Note(models.Model):
    description = models.TextField(validators=[validate_min_length])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50]
