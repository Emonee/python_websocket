import json
from random import randint
from os import getenv
from websockets.asyncio.server import broadcast

from custom_exceptions import InvalidAction
from game import Game

MAX_ROOMS = int(getenv("MAX_ROOMS", 10))
ROOMS = {}

class Room:
    def __init__(self, name, user):
        if self.full_rooms():
            raise Exception("Maximum number of rooms reached")
        if len(name) > 15:
            raise ValueError("Room's name must be less than 15 characters")
        self.id = f"{randint(0, 9999):04}"
        self.name = name
        self.users = {user}
        self.game = None
        ROOMS[self.id] = self
    
    def __str__(self):
        return f"{self.name}: {self.users}"
    
    @staticmethod
    def full_rooms():
        return len(ROOMS) >= MAX_ROOMS
    
    @staticmethod
    def get_rooms():
        return ROOMS
    
    @staticmethod
    def find_room(id):
        return ROOMS[id]
    
    def broadcast_room(self, message):
        broadcast(self.room_sockets(), json.dumps(message)) # type: ignore
    
    def room_sockets(self):
        return [user.socket for user in self.users if user.socket]

    def add_user(self, user):
        self.users.add(user)
        self.broadcast_room({
            'action': 'user_joined',
            'data': {
                'user_name': user.name,
                'user_tag': user.tag
            }
        })

    def remove_user(self, user):
        if user in self.users: self.users.remove(user)
        if len(self.users) < 1:
            del ROOMS[self.id]
            return
        self.broadcast_room({
            'action': 'user_left',
            'data': {
                'user_name': user.name,
                'user_tag': user.tag
            }
        })

    def start_game(self):
        # if len(self.users) < 2: raise InvalidAction("Not enough users to start a game")
        self.game = Game(list(self.users))
        return self.game
