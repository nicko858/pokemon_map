import folium
import json
import pytz

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
import os

MOSCOW_CENTER = (55.751244, 37.618423)
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)
CURRENT_TZ = pytz.timezone('Europe/Moscow')


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = localtime(timezone=CURRENT_TZ)
    pokemons_entitys = PokemonEntity.objects.filter(
        disappeared_at__gt=now,
        appeared_at__lt=now,
        )
    zoom_start = 12
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=zoom_start)
    pokemons_on_page = []
    for pokemon_entity in pokemons_entitys:
        img_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url,
            )
        pokemons_on_page.append({
            'pokemon_id': pokemon_entity.pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon_entity.pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    zoom_start = 12
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=zoom_start)
    pokemon_entity = PokemonEntity.objects.get(pokemon=int(pokemon_id))
    add_pokemon(
        folium_map, pokemon_entity.lat,
        pokemon_entity.lon,
        request.build_absolute_uri(pokemon.image.url),
    )
    serialized_pokemon = {
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_jp': pokemon.title_jp,
        'title_en': pokemon.title_en,
        }


    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': serialized_pokemon,
    })
