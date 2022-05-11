from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(default=False, max_length=100)
    image = models.ImageField(upload_to='pokemons', null=True)

    def __str__(self):
        return '{}'.format(self.title)
