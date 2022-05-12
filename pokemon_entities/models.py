from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(default=False, max_length=100)
    image = models.ImageField(upload_to='pokemons', blank=True)
    description = models.TextField(blank=True)
    title_jp = models.CharField(blank=True, max_length=100)
    title_en = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return '{0}'.format(self.title)


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True, default=False)
    lon = models.FloatField(null=True, default=False)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(default=None)
    disappeared_at = models.DateTimeField(default=None)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)
