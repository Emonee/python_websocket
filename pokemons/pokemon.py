from random import randint
import os

class Pokemon:
    def __init__(self, name, sprite, type1, type2, habitat, colors, evolution_stage, height, weight):
        self.name = name
        self.sprite = sprite
        self.type1 = type1
        self.type2 = type2
        self.habitat = habitat
        self.colors = colors
        self.evolution_stage = evolution_stage
        self.height = height
        self.weight = weight

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_random():
        with open(os.path.join(os.path.dirname(__file__), 'pokemons.csv')) as f:
            pokemons = f.readlines()
            random_number = randint(1, len(pokemons))
        return Pokemon.get_by_number(random_number)
    
    @staticmethod
    def get_by_number(number):
        with open(os.path.join(os.path.dirname(__file__), 'pokemons.csv')) as f:
            pokemons = f.readlines()
            random_pokemon = pokemons[number].split(',')
        return Pokemon(
            random_pokemon[0],
            random_pokemon[1],
            random_pokemon[2],
            random_pokemon[3],
            random_pokemon[4],
            random_pokemon[5],
            int(random_pokemon[6]),
            float(random_pokemon[7]),
            float(random_pokemon[8])
        )
