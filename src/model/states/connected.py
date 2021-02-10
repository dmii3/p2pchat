from __future__ import annotations

from src.model.states.state import State
from src.model.states.statetype import StateType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.p2pchat import P2PChat


class ConnectedState(State):
    def __init__(self, context: P2PChat):
        self.__context = context

    def connect_to(self, host, port) -> None:
        raise RuntimeError("You are already connected!")

    def disconnect(self) -> None:
        self.__context.connection.close()
        self.__context.transition_to(StateType.LISTENING)

    def send_message(self, message: str) -> None:
        self.__context.connection.send_data(message.encode('utf-8'))

    def send_file(self, filename: str) -> None:
        raise NotImplementedError()

    def update(self):
        connection = self.__context.connection
        if connection.is_open():
            if connection.readable():
                received_data = connection.recv_data()
                self.__context.controller.new_message(received_data.decode('utf-8'), True)
            else:
                print("8S")
        else:
            self.__context.transition_to(StateType.LISTENING)



