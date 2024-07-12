import asyncio
import websockets
import logging
import json

logging.basicConfig(level=logging.INFO)

async def connect(uri):
    while True:
        try:
            logging.info(f"Connecting to {uri}")
            async with websockets.connect(uri) as websocket:
                logging.info(f"Connected to {uri}")
                stop_event = asyncio.Event()
                await asyncio.gather(
                    handle_messages(websocket, stop_event),
                    process_messages(websocket, stop_event)
                )
        except (websockets.ConnectionClosed, ConnectionRefusedError) as e:
            logging.error(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            await asyncio.sleep(5)

async def handle_messages(websocket, stop_event):
    global is_interrupt

    while not stop_event.is_set():
        try:
            message = await websocket.recv()
            # logging.info(f"handle_messages queue----> Received message: {message}")

        except websockets.ConnectionClosed as e:
            stop_event.set()
            logging.warning(f"handle_messages Connection closed: {e}")

        message_dict = json.loads(message)
        if message_dict.get('event') == 1002006:
            print(f'------------server wanna interrup-----')
            is_interrupt = True
        else:
            await message_queue.put(message)


async def process_messages(websocket, stop_event):
    global is_interrupt

    while not stop_event.is_set():
        # Process the message here
        try:
            message = await message_queue.get()
            # print(f'process_messages:{message}')

            for i in range(5):
                if is_interrupt:
                    print(f'hahahahahhha----------I am release')
                    break
                await asyncio.sleep(1)

            if is_interrupt:
                is_interrupt = False
                print(f'--------interrupt sending...')
                await websocket.send("I was interupted!!!!!")
            else:
                print(f'+++++++ normal message sending...')
                await websocket.send("I sleep for a long time ^^")
        except websockets.ConnectionClosed as e:
            stop_event.set()
            logging.warning(f"process_messages Connection closed: {e}")


async def main():
    global message_queue
    global is_interrupt
    message_queue = asyncio.Queue()
    is_interrupt = False
    uri = "ws://localhost:7777/ws"
    await connect(uri)

if __name__ == "__main__":
    asyncio.run(main())
