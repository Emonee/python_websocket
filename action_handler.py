import json

from custom_exceptions import InvalidAction

async def main_handler(message, room, user):
    try:
        action = message.get('action')
        if action == 'start_game': start_game(room)
        if action == 'play': play(room, user, message)
    except InvalidAction as e:
        await user.send_message(json.dumps({
            'error': True,
            'message': str(e)
        }))
    except Exception as e:
        await user.send_message(json.dumps({
            'error': True,
            'message': 'Unknown error'
        }))

def start_game(room):
    room.start_game()
    room.broadcast_room({
        'action': 'start_game',
        'data': {
            'room_name': room.name,
            'room_id': room.id
        }
    })

def play(room, user, message):
    pokemon_number = message['data']['pokemon_number']
    if not room.game: raise InvalidAction("Game is not started")
    play = room.game.play(user, pokemon_number)
    room.broadcast_room({
        'action': 'play',
        'data': play.to_dict()
    })