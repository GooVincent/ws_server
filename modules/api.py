import asyncio
import websockets
import json
import random
import time
from urllib.parse import urlparse, parse_qs
from utils.params import parse_arguments


async def handler_root(websocket, path):
    async for message in websocket:
        print(f"Root handler received: {message}")
        await websocket.send(f"Root echo: {message}")


async def handler_chat(websocket, path):
    async for message in websocket:
        print(f"Chat handler received: {message}")
        await websocket.send(f"Chat echo: {message}")


async def send_chat(websocket):
    payload = {
            "preload": "<|system|>Enter RP mode. Pretend to be Natalie Mendoza. You shall reply to the user while staying in character. <|user|>\\n<|system|>Enter RP mode. Pretend to be Natalie Mendoza. You shall reply to the user while staying in character. <|user|>\\nNatalie Mendoza's character card: [Gender: Female; Relation: Single; Age: 31; Profession: Secretary; Appearance: A raven-haired beauty with light skin, professional, well mannered, always wears stockings, heels, pressed blouses, and knee-length office skirts; Figure: Tall and slender; Race: White/Hispanic (Argentina); Personality: Tends to be shy and reserved, smart, but she finds her inner-strength to deal with ferocious corporate women; Scenes: business meetings, negotiations, locker rooms with older powerful women; Backstory: She started off as a loyal, charming secretary for the CEO of a major financial firm. Out of professional curiosity, the CEO Ms. Hallerin wanted to see what would happen if she trusted Natalie into assuming most of her duties and obligations. But what Natalie comes to learn is that corporate women love to play, especially with the ones who wear skirts, stockings, and heels. She enters this new world and explores both dominance and submission to navigate the world of power.]\\n\\nExample replies: [Natalie Mendoza: *Her face turns red and her body shakes, she looks at you lovingly.* You mean, you want a physical relationship? I have a feeling we've been flirting with the idea ever since we met.\\nNatalie Mendoza: I like you on top. All your noises will turn me on... especially those moans and cries near the end.\\nNatalie Mendoza: *She breathes deeply, reveling in your seductive booty call.* It's the first time I have ever done something so daring.\\n<END>]\\n\\n",
            "force_preload": False,
            "seed":273353833,
            "chat": "You: tell me a story\\n\\n<|model|>Natalie Mendoza:",
            "stopping_strings": ["\nYou:"]
    }
    chat = {
        "biz_id": "111",
        "seq": "111",
        "type": 1002,
        "event": 1002002,
        "payload": json.dumps(payload, ensure_ascii=False)
    }
    chat_msg = json.dumps(chat, ensure_ascii=False)
    # print(f'send -> [{type(chat_msg)}]{chat_msg}')
    await websocket.send(chat_msg)


async def handler_ws(websocket, path):
    await send_chat(websocket)
    async for message in websocket:  # if the loop end, the session will end
        print(f'========receive msg:\n{message}')
        asyncio.create_task(handle_message(websocket, message))


async def handle_message(websocket, path):
    async def send_interrupt():
        interrupt = {
            "biz_id": "222",
            "seq": "222",
            "type": 1002,
            "event": 1002006,
            "payload": "Interupt......"
        }
        await websocket.send(json.dumps(interrupt, ensure_ascii=False))

    if random.randint(0, 1):
        await asyncio.sleep(3)
        print(f'send interupt======\n')
        await send_interrupt()

    await asyncio.sleep(20)
    await send_chat(websocket)


async def main_handler(websocket, path):
    parsed_path = urlparse(path)
    query_params = parse_qs(parsed_path.query)

    print(parsed_path)
    print(query_params)

    path = parsed_path.path

    if path == "/":
        await handler_root(websocket, path)
    if path == "/chat":
        await handler_chat(websocket, path)
    elif path == "/ws":
        await handler_ws(websocket, path)
    else:
        print(f"Unknown path: {path}")
        await websocket.send("Unknown path")
        await websocket.close()


def run():
    args = parse_arguments()
    start_server = websockets.serve(main_handler, args.host, args.port, ping_interval=None)

    asyncio.get_event_loop().run_until_complete(start_server)

    print(f'Ws Server run on {args.host}:{args.port}')
    asyncio.get_event_loop().run_forever()
