from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )
    avatar_url = models.URLField(null=True, blank=True)


