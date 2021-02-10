from __future__ import annotations

from typing import Dict, Callable, TYPE_CHECKING
from src.model.states.connected import ConnectedState
from src.model.states.connecting import ConnectingState
from src.model.states.listening import ListeningState
from src.model.states.receivedconnection import ReceivedConnectionState
from src.model.states.statetype import StateType

if TYPE_CHECKING:
    from src.model.p2pchat import P2PChat
    from src.model.states.state import State


class StateFactory:
    __states: Dict[StateType, Callable[[P2PChat], State]] = {
        StateType.CONNECTED: (lambda context: ConnectedState(context)),
        StateType.CONNECTING: (lambda context: ConnectingState(context)),
        StateType.LISTENING: (lambda context: ListeningState(context)),
        StateType.RECEIVED_CONNECTION: (lambda context: ReceivedConnectionState(context))
    }

    def __init__(self):
        pass

    def get_state(self, state_type: StateType, context: P2PChat) -> State:
        return self.__states[state_type](context)
