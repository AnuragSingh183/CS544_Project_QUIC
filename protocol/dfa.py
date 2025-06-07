from protocol.constants import ProtocolState, MessageType

def get_next_state(current_state, message_type):
    if current_state == ProtocolState.INIT and message_type == MessageType.AUTH:
        return ProtocolState.AUTHENTICATED
    if current_state == ProtocolState.AUTHENTICATED and message_type == MessageType.STREAM_START:
        return ProtocolState.STREAMING
    if current_state == ProtocolState.STREAMING and message_type == MessageType.PLAYBACK_CTRL:
        return ProtocolState.STREAMING
    if message_type == MessageType.STOP or message_type == MessageType.ERROR:
        return ProtocolState.TERMINATED
    return None
