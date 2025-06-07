from protocol.constants import *
from protocol.dfa import get_next_state

def handle_message(msg_type, state, payload=None):
    print(f"[DEBUG] State: {state.name}, Msg: {msg_type}")
    
    next_state = get_next_state(state, msg_type)
    if next_state is None:
        return MessageType.ERROR, ProtocolState.TERMINATED, b"Invalid state transition."

    # Simulated payload response
    if msg_type == MessageType.HELLO:
        return msg_type, state, b"HELLO_ACK"
    elif msg_type == MessageType.AUTH:
        if payload == b"admin:pass123":
            return msg_type, next_state, b"AUTH_SUCCESS"
        else:
            return MessageType.ERROR, ProtocolState.TERMINATED, b"AUTH_FAILED"
    elif msg_type == MessageType.STREAM_START:
        return msg_type, next_state, b"STREAM_STARTED"
    elif msg_type == MessageType.PLAYBACK_CTRL:
        return msg_type, next_state, b"PLAYBACK_ACK"
    elif msg_type == MessageType.STOP:
        return msg_type, next_state, b"STOP_ACK"
    else:
        return MessageType.ERROR, ProtocolState.TERMINATED, b"UNKNOWN_COMMAND"
