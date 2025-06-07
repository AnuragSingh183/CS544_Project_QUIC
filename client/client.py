import sys
import os
import traceback
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import argparse
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from protocol.constants import *


# function to send a message to the server
async def send_message(writer, msg_type, payload=b""):
    print(f"Sending message type {msg_type} with payload: {payload.decode(errors='ignore')}")
    writer.write(msg_type.to_bytes(1, 'big') + payload.ljust(64, b' '))
    await writer.drain()


#function that connects to the QUIC server and communicates using defined message types
async def main(host, port):
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False  # Accept self-signed cert
    config.alpn_protocols = ["qstream"]
    print("⚙️  Using config:", config.__dict__)

    print(f"🔗 Connecting to {host}:{port}...")

    try:
         # Establish QUIC connection to server
        async with connect(host, port, configuration=config) as client:
            print("Connected to QUIC server.")
            stream_id = client._quic.get_next_available_stream_id()
            reader, writer = await client.create_stream(stream_id)
            print(f"Stream {stream_id} opened.")

            await send_message(writer, MessageType.HELLO)
            await asyncio.sleep(0.5)

            await send_message(writer, MessageType.AUTH, b"admin:pass123")
            await asyncio.sleep(0.5)

            await send_message(writer, MessageType.STREAM_START)
            await asyncio.sleep(0.5)

            await send_message(writer, MessageType.PLAYBACK_CTRL)
            await asyncio.sleep(0.5)

            await send_message(writer, MessageType.STOP)

            writer.write_eof()
            print("📡 Awaiting server responses...\n")


           
           # Read and print messages from server until the stream ends
            while not reader.at_eof():
                line = await reader.readline()
                if not line:
                    break
                print(" Server:", line.decode().strip())

            print("Stream closed by server.")

    except Exception as e:
        print(" Connection or stream error occurred.")
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    asyncio.run(main(args.host, args.port))
