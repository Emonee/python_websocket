import asyncio
import json
from urllib.parse import parse_qs, urlparse
from websockets.asyncio.server import serve
from http import HTTPStatus
import os

from action_handler import main_handler
from room import Room
from user import User

port = int(os.getenv("PORT", 5000))

def health_check(connection, request):
    if request.path == "/healthz":
        response = connection.respond(HTTPStatus.OK, "OK")
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response

async def handler(websocket):
    parsed_url = urlparse(websocket.request.path)
    query_params = parse_qs(parsed_url.query)
    user_name = query_params.get("user_name", [None])[0]
    room_name = query_params.get("room_name", [None])[0]
    room_id = query_params.get("room_id", [None])[0]
    try:
        user = User(user_name, websocket)
        room = Room.find_room(room_id) if room_id else Room(room_name, user)
        if not room: raise Exception("Room not found")
    except Exception as e:
        user.disconnect()
        await websocket.close(reason=str(e))
        return
    if room_name: await user.send_message(json.dumps({
        'action': 'start_room',
        'data': {
            'room_name': room.name,
            'room_id': room.id,
            'initial_player': {
                'user_name': user.name,
                'user_tag': user.tag
            }
        }
    }))
    elif room_id:
        await user.send_message(json.dumps({
            'action': 'room_users',
            'data': {
                'room_name': room.name,
                'room_id': room.id,
                'users': [{ 'user_name': user.name, 'user_tag': user.tag } for user in room.users]
            }
        }))
        room.add_user(user)
    async for json_message in websocket:
        message = json.loads(json_message)
        await main_handler(message, room, user)
    user.disconnect()

async def main():
    async with serve(handler, "0.0.0.0", port, process_request=health_check):
        print(f"App running at 0.0.0.0:{port}")
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
