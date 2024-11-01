from custom_exceptions import InvalidAction
from pokemons.pokemon import Pokemon

class Game:
    def __init__(self, players):
        self.players = players
        self.pokemon = Pokemon.get_random()
        self.turn = 0
        self.player_in_turn_index = 0
        self.winner = None
        self.plays = []

    def play(self, player, pokemon_number):
        if self.winner: raise InvalidAction("Game is over")
        if self.players[self.player_in_turn_index] != player: raise InvalidAction("It's not your turn")
        play = Play(player, pokemon_number, self.pokemon)
        self.plays.append(play)
        self.turn += 1
        if self.player_in_turn_index == len(self.players) - 1: self.player_in_turn_index = 0
        else: self.player_in_turn_index += 1
        if play.pokemon.name == self.pokemon.name: self.winner = player
        return play

class Play:
    def __init__(self, player, pokemon_number, game_pokemon):
        self.player = player
        self.pokemon = Pokemon.get_by_number(pokemon_number)
        self.match_type1 = 'match' if self.pokemon.type1 == game_pokemon.type1 else 'partial' if self.pokemon.type1 in game_pokemon.type2 else 'no_match'
        self.match_type2 = 'match' if self.pokemon.type2 == game_pokemon.type2 else 'partial' if self.pokemon.type2 in game_pokemon.type1 else 'no_match'
        self.match_habitat = self.pokemon.habitat == game_pokemon.habitat
        self.match_colors = self.pokemon.colors == game_pokemon.colors
        self.match_evolution_stage = self.pokemon.evolution_stage == game_pokemon.evolution_stage
        self.height_comparison = 'match' if self.pokemon.height == game_pokemon.height else 'taller' if self.pokemon.height > game_pokemon.height else 'shorter'
        self.weight_comparison = 'match' if self.pokemon.weight == game_pokemon.weight else 'heavier' if self.pokemon.weight > game_pokemon.weight else 'lighter'
        self.winning_play = self.pokemon.name == game_pokemon.name
    
    def to_dict(self):
        return {
            'player': { 'name': self.player.name, 'tag': self.player.tag },
            'pokemon': self.pokemon.__dict__,
            'matching_results': {
                'type1': self.match_type1,
                'type2': self.match_type2,
                'habitat': self.match_habitat,
                'colors': self.match_colors,
                'evolution_stage': self.match_evolution_stage,
                'height_comparison': self.height_comparison,
                'weight_comparison': self.weight_comparison
            },
            'winning_play': self.winning_play
        }