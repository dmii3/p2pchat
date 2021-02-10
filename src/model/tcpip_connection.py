from src.model.connection import Connection
# from src.model.utils.observable import Observable
from src.model.utils.observer import Observer

import socket as s
from select import select
from threading import Thread, Lock
from typing import Set, Sequence, List, Tuple
from time import sleep


class TCPIPConnection(Connection, Thread):
    def __init__(self, inbound_port=8888):
        Connection.__init__(self)
        Thread.__init__(self)
        self.__observers: Set[Observer] = set()
        self.__inbound_port = inbound_port

        self.__set_up_listen_socket()
        self.__connected = False
        self.__connecting = False
        self.__connection_waiting = False
        self.__host = None  # type: s.socket
        self.__addr = None

        self.__lock = Lock()
        self.__running = False
        self.__state_changed = False

        self.__recv_buffer = bytearray()

    def __set_up_listen_socket(self):
        self.__listen_socket = s.socket()
        self.__listen_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.__listen_socket.bind(('0.0.0.0', self.__inbound_port))
        self.__listen_socket.listen(1)
        self.__listening = True

    def open(self, host: str, port: int) -> None:
        self.__host = s.socket()
        self.__host.connect((host, port))
        self.__listen_socket.close()
        self.__listen_socket = None  # type: s.socket
        self.__listening = False
        self.__connecting = True

    def close(self) -> None:
        self.__connected = False
        self.__connecting = False
        self.__host.close()
        self.__host = None  # type: s.socket
        self.__addr = None
        self.__set_up_listen_socket()
        self.__listening = True

    def send_data(self, data: bytes) -> None:
        self.__host.send(data)

    def recv_data(self) -> bytearray:
        ret = self.__recv_buffer.copy()
        self.__recv_buffer.clear()
        return ret

    def accept_connection(self) -> None:
        self.__host.send(b'123')
        self.__connecting = False
        self.__listening = False
        self.__connection_waiting = False
        self.__connected = True

    def decline_connection(self) -> None:
        self.close()
        self.__connection_waiting = False

    def is_open(self) -> bool:
        return self.__connected

    def readable(self) -> bool:
        return len(self.__recv_buffer) != 0

    def has_incoming_connection(self) -> bool:
        return self.__connection_waiting

    def get_incoming_connection_address(self) -> Tuple[str, int]:
        return self.__addr

    def register_observer(self, observer: Observer) -> None:
        self.__lock.acquire()
        self.__observers.add(observer)
        self.__lock.release()

    def remove_observer(self, observer: Observer) -> None:
        self.__lock.acquire()
        self.__observers.remove(observer)
        self.__lock.release()

    def notify_observers(self) -> None:
        for o in self.__observers:
            o.update()
        self.__state_changed = False

    def run(self) -> None:
        self.__running = True

        while self.__running:
            self.__lock.acquire()
            if self.__listening:
                self.__handle_listening()
            elif self.__connected:
                self.__handle_connected()
            elif self.__connecting:
                self.__handle_connecting()

            if self.__state_changed:
                self.notify_observers()

            self.__lock.release()

            sleep(0.05)

        if self.__host is not None:
            self.__host.close()
        if self.__listen_socket is not None:
            self.__listen_socket.close()

    def lock(self) -> None:
        self.__lock.acquire()

    def unlock(self) -> None:
        self.__lock.release()

    def stop(self) -> None:
        self.__running = False

    def __handle_listening(self) -> None:
        readable = self.__get_readable([self.__listen_socket])
        if readable:
            self.__host, self.__addr = self.__listen_socket.accept()
            self.__listen_socket.close()
            self.__listen_socket = None  # type: s.socket
            self.__listening = False
            self.__connection_waiting = True
            self.__state_changed = True

    def __handle_connected(self) -> None:
        readable = self.__get_readable([self.__host])
        while readable:
            self.__state_changed = True
            data = self.__host.recv(1024)
            if not data:

                self.close()
                break

            self.__recv_buffer += data
            readable = self.__get_readable([self.__host])

    def __handle_connecting(self) -> None:
        readable = self.__get_readable([self.__host])
        if readable:
            response = self.__host.recv(100)
            if not response:
                self.__host.close()
                self.__host = None  # type: s.socket
                self.__addr = None
                self.__set_up_listen_socket()
            else:
                self.__connecting = False
                self.__connected = True
            self.__state_changed = True

    def __get_readable(self, sockets: Sequence[s.socket]) -> List[s.socket]:
        return select(sockets, [], [], 0.0)[0]
