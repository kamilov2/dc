from django.db import models
from django.utils import timezone

class Profile(models.Model):
    name = models.TextField(verbose_name="User Name", max_length=150)
    device_id = models.TextField(verbose_name="Device ID", blank=True, max_length=256, unique=True)
    permission = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.name} ({self.device_id[:8]}) - Permission: {self.permission}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['permission']),
            models.Index(fields=['created_at']),

        ]
