import requests
import os

poke_api_uri = "https://pokeapi.co/api/v2/"

def main():
    for num in range(1, 152):
        pokemon = requests.get(f"{poke_api_uri}pokemon/{num}").json()
        specie = requests.get(pokemon['species']['url']).json()
        evolution_chain = requests.get(specie['evolution_chain']['url']).json()
        print(pokemon['name'])
        with open(os.path.join(os.path.dirname(__file__), 'pokemons.csv'), "a") as f:
            try:
                type2 = pokemon['types'][1]['type']['name']
            except:
                type2 = None
            f.write(f"\n{pokemon['name']},{pokemon['sprites']['front_default']},{pokemon['types'][0]['type']['name']},{type2},{specie['habitat']['name']},{specie['color']['name']},{get_evolution_stage(evolution_chain, pokemon['name'])},{pokemon['height'] * 10 / 100},{pokemon['weight'] * 100 / 1000}")

def get_evolution_stage(evolution_chain, name):
    if len(evolution_chain['chain']['evolves_to']) < 1: return 1
    baby_modifier = 1 if evolution_chain['chain']['is_baby'] else 0
    if evolution_chain['chain']['species']['name'] == name: return 1
    if evolution_chain['chain']['evolves_to'][0]['species']['name'] == name: return 2 - baby_modifier
    return 3 - baby_modifier


if __name__ == "__main__":
    main()