from abc import ABC, abstractmethod
from src.model.utils.observable import Observable
from typing import Tuple


class Connection(Observable, ABC):
    @abstractmethod
    def open(self, host: str, port: int) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def send_data(self, data: bytes) -> None:
        pass

    @abstractmethod
    def recv_data(self) -> bytearray:
        pass

    @abstractmethod
    def accept_connection(self) -> None:
        pass

    @abstractmethod
    def decline_connection(self) -> None:
        pass

    @abstractmethod
    def is_open(self) -> bool:
        pass

    @abstractmethod
    def readable(self) -> bool:
        pass

    @abstractmethod
    def has_incoming_connection(self) -> bool:
        pass

    @abstractmethod
    def get_incoming_connection_address(self) -> Tuple[str, int]:
        pass
