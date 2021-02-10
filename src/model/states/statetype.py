from enum import Enum, auto


class StateType(Enum):
    LISTENING = auto(),
    CONNECTING = auto(),
    RECEIVED_CONNECTION = auto(),
    CONNECTED = auto(),
    CONNECTION_CLOSING = auto()