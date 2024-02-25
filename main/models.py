import os
import uuid
import secrets
import random
from django.db import models



def upload_media_path(instance, filename):
    unique_filename = f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"
    secret_key = secrets.token_hex(random.randint(0,15))

    return os.path.join(f'{secret_key}', unique_filename)

class Photo(models.Model):
    name = models.CharField(verbose_name="Name", max_length=256)
    photo = models.ImageField(verbose_name="Photo", upload_to=upload_media_path)
    class Meta:
        indexes = [
            models.Index(fields=['name']), 
            ]

    def __str__(self):
        return self.name
