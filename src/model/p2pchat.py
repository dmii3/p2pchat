from __future__ import annotations

from src.model.states.statetype import StateType
from src.model.states.factory import StateFactory
from src.model.utils.observer import Observer
from src.model.tcpip_connection import TCPIPConnection
from src.model.connection import Connection
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controller.mainwindowcontroller import MainWindowController


class P2PChat(Observer):
    def __init__(self, state_factory: StateFactory, inbound_port):
        self.__controller = None  # type: MainWindowController
        self.__connection = TCPIPConnection(inbound_port)
        self.__connection.register_observer(self)
        self.__connection.start()

        self.__state_factory = state_factory
        self.__state = self.__state_factory.get_state(StateType.LISTENING, self)

    @property
    def connection(self) -> Connection:
        return self.__connection

    @property
    def controller(self) -> MainWindowController:
        return self.__controller

    def set_controller(self, controller: MainWindowController) -> None:
        self.__controller = controller

    def connect_to(self, host: str, port: int) -> None:
        self.__synchronized_call(self.__state.connect_to, host, port)

    def disconnect(self) -> None:
        self.__synchronized_call(self.__state.disconnect)

    def send_message(self, message: str) -> None:
        self.__synchronized_call(self.__state.send_message, message)

    def send_file(self, filename: str) -> None:
        self.__synchronized_call(self.__state.send_file, filename)

    def accept_connection(self) -> None:
        self.__synchronized_call(self.__state.accept_connection)

    def decline_connection(self) -> None:
        self.__synchronized_call(self.__state.decline_connection)

    def transition_to(self, new_state_type: StateType) -> None:
        self.__state = self.__state_factory.get_state(new_state_type, self)

    def update(self) -> None:
        self.__state.update()

    def exit(self) -> None:
        self.__connection.stop()

    def __synchronized_call(self, function, *args) -> any:
        try:
            self.__connection.lock()
            ret_val = function(*args)
            return ret_val
        finally:
            self.__connection.unlock()


