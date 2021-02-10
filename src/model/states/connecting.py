from __future__ import annotations

from src.model.states.state import State
from src.model.states.statetype import StateType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.p2pchat import P2PChat


class ConnectingState(State):
    def __init__(self, context: P2PChat):
        self.__context = context

    def connect_to(self, host, port) -> None:
        pass

    def disconnect(self) -> None:
        self.__context.connection.close()
        self.__context.transition_to(StateType.LISTENING)

    def send_message(self, message: str) -> None:
        raise RuntimeError("You are still connecting")

    def send_file(self, filename: str) -> None:
        raise NotImplementedError()

    def update(self):
        connection = self.__context.connection
        if connection.is_open():
            self.__context.transition_to(StateType.CONNECTED)
        else:
            self.__context.transition_to(StateType.LISTENING)
