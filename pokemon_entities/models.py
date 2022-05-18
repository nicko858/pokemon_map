from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(
        'русское название',
        max_length=100,
        )
    img_url = models.ImageField(
        'путь к картинке',
        upload_to='pokemons',
        blank=True,
        )
    description = models.TextField('описание', blank=True)
    title_jp = models.CharField(
        'японское название',
        blank=True,
        max_length=100,
        )
    title_en = models.CharField(
        'английское название',
        blank=True,
        max_length=100,
        )
    previous_evolution = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.SET_NULL,
        related_name='next_evolutions',
        verbose_name='из кого эволюционировал',
        )

    def __str__(self):
        return '{0}'.format(self.title_ru)


class PokemonEntity(models.Model):
    lat = models.FloatField('широта', null=True, default=False)
    lon = models.FloatField('долгота', null=True, default=False)
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='покемон',
        )
    appeared_at = models.DateTimeField('когда появится', default=None)
    disappeared_at = models.DateTimeField('когда исчезнет', default=None)
    level = models.IntegerField('уровень', default=0)
    health = models.IntegerField('здоровье', default=0)
    strength = models.IntegerField('сила', default=0)
    defence = models.IntegerField('защита', default=0)
    stamina = models.IntegerField('выносливость', default=0)
