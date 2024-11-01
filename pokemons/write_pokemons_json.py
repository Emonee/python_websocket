import json
import os
import csv

json_pokemons = {}
with open(os.path.join(os.path.dirname(__file__), 'pokemons.csv')) as f:
    pokemons = csv.reader(f)
    next(pokemons)
    num = 1
    for pokemon in pokemons:
        json_pokemons[num] = {
            'id': num,
            'name': pokemon[0],
            'sprite': pokemon[1]
        }
        num += 1
        
with open(os.path.join(os.path.dirname(__file__), 'pokemons.json'), 'w') as f:
    json.dump({"pokemons": json_pokemons}, f)
