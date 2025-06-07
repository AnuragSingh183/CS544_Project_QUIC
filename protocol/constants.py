


from enum import Enum, auto

class ProtocolState(Enum):
    INIT = auto()
    AUTHENTICATED = auto()
    STREAMING = auto()
    TERMINATED = auto()

class MessageType:  
    HELLO = 0x01
    AUTH = 0x02
    STREAM_START = 0x04
    PLAYBACK_CTRL = 0x05
    STREAM_DATA = 0x07
    STOP = 0x08
    ERROR = 0x09

class PlaybackCommand:
    PLAY = 0x01
    PAUSE = 0x02
    SEEK = 0x03
    STOP = 0x04
