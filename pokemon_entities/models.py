from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(default=False, max_length=100)
