import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from aioquic.asyncio import serve, QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from protocol.constants import *
from protocol.handler import handle_message
from protocol.dfa import ProtocolState

# Define the server-side QUIC protocol handler
class QStreamServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = ProtocolState.INIT

    # This method handles individual bidirectional streams from clients
    async def stream_handler(self, stream_id, reader, writer):
        print(f"🔌 New stream opened: {stream_id}")
        try:
            while True:
                msg_type_byte = await reader.read(1)
                if not msg_type_byte:
                    break
                msg_type = int.from_bytes(msg_type_byte, byteorder='big')
                payload = await reader.read(64)
                msg_type, new_state, response = handle_message(msg_type, self.state, payload.strip())
                self.state = new_state
                writer.write(response + b"\n")
                await writer.drain()
                
                 # Terminate the connection if protocol reaches final state
                if new_state == ProtocolState.TERMINATED:
                    break
        except Exception as e:
            writer.write(f"ERROR: {str(e)}".encode() + b"\n")


async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain("server/cert.pem", "server/key.pem")
    config.alpn_protocols = ["qstream"]

    print("🔧 Starting QUIC server on 0.0.0.0:8843 (UDP)...")
    server = await serve(
        host="0.0.0.0",
        port=9000,
        configuration=config,
        create_protocol=QStreamServerProtocol
    )
    print("✅ Server is running on QUIC port 9000 and ready to accept connections.")

    # Keep the server running forever
    await asyncio.Event().wait()



if __name__ == "__main__":
    asyncio.run(main())
