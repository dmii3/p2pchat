from __future__ import annotations

from src.model.states.state import State
from src.model.states.statetype import StateType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.p2pchat import P2PChat


class ReceivedConnectionState(State):
    def __init__(self, context: P2PChat):
        self.__context = context

    def connect_to(self, host, port) -> None:
        raise RuntimeError("You have incoming connection")

    def disconnect(self) -> None:
        pass

    def send_message(self, message: str) -> None:
        raise RuntimeError("You have incoming connection")

    def send_file(self, filename: str) -> None:
        raise NotImplementedError()

    def update(self):
        raise RuntimeError("update in received conn")

    def accept_connection(self) -> None:
        self.__context.connection.accept_connection()
        self.__context.transition_to(StateType.CONNECTED)

    def decline_connection(self) -> None:
        self.__context.connection.decline_connection()
        self.__context.transition_to(StateType.LISTENING)
