from __future__ import annotations

from src.model.states.state import State
from src.model.states.statetype import StateType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.p2pchat import P2PChat


class ListeningState(State):
    def __init__(self, context: P2PChat):
        self.__context = context

    def connect_to(self, host, port) -> None:
        try:
            self.__context.connection.open(host, port)
        except IOError as e:
            raise RuntimeError(str(e))

        self.__context.transition_to(StateType.CONNECTING)

    def disconnect(self) -> None:
        raise RuntimeError("You are not connected")

    def send_message(self, message: str) -> None:
        raise RuntimeError("You are not connected")

    def send_file(self, filename: str) -> None:
        raise NotImplementedError()

    def update(self):
        connection = self.__context.connection
        assert (connection.has_incoming_connection())
        self.__context.controller.incoming_connection(connection.get_incoming_connection_address()[0])
        self.__context.transition_to(StateType.RECEIVED_CONNECTION)
