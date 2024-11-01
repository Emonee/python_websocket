from os import getenv
import random

from room import ROOMS

MAX_USERS = int(getenv("MAX_USERS", 10))
CONNECTED_USERS = {}

class User:
    def __init__(self, name, socket):
        if self.full_users():
            raise Exception("Maximum number of users reached")
        if len(name) > 15:
            raise ValueError("User's name must be less than 15 characters")
        self.name = name or 'Guest'
        self.socket = socket
        self.tag = f"{random.randint(0, 9999):04}"
        CONNECTED_USERS[self.tag] = self

    def __str__(self):
        return f"{self.name}#{self.tag}"
    
    @staticmethod
    def connected_users():
        return CONNECTED_USERS

    @staticmethod
    def full_users():
        return len(CONNECTED_USERS) >= MAX_USERS
    
    async def send_message(self, message):
        if self.socket: await self.socket.send(message)
    
    def disconnect(self):
        for room in list(ROOMS.values()): room.remove_user(self)
        del CONNECTED_USERS[self.tag]
