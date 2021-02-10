from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def connect_to(self, host, port) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def send_message(self, message: str) -> None:
        pass

    @abstractmethod
    def send_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def update(self):
        pass

    def accept_connection(self) -> None:
        pass

    def decline_connection(self) -> None:
        pass
