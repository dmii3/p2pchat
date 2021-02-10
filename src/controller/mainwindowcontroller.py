from src.model.p2pchat import P2PChat
from src.view.mainwindow import MainWindow
from PySide2.QtCore import Signal, QObject

from time import strftime


class Signals(QObject):
    new_message = Signal(str)
    error = Signal(str)
    my_address = Signal(str)
    incoming_connection = Signal(str)


class MainWindowController:
    def __init__(self, model: P2PChat, view: MainWindow):
        self.__model = model
        self.__model.set_controller(self)
        self.__view = view
        self.__view.set_controller(self)
        self.__signals = Signals()

        self.__signals.new_message.connect(self.__view.update_chat_history)
        self.__signals.incoming_connection.connect(self.__view.show_connection_dialog)
        self.__signals.error.connect(self.__view.show_message_box)

    def connect_clicked(self, host: str, port: str) -> None:
        port_int = int(port)
        try:
            self.__model.connect_to(host, port_int)
        except RuntimeError as e:
            self.__signals.error.emit(str(e))

    def send_clicked(self, message: str) -> None:
        self.__view.text_edit_new_message.clear()
        try:
            self.__model.send_message(message)
        except RuntimeError as e:
            self.__signals.error.emit(str(e))
            return
        self.new_message(message, False)

    def form_closed(self) -> None:
        self.__model.exit()

    def new_message(self, message: str, incoming: bool) -> None:
        current_time = strftime("[%H:%m:%S]")
        if incoming:
            a = '[I]: '
        else:
            a = '[O]: '
        res_str = ''.join([current_time, a, message])
        self.__signals.new_message.emit(res_str)

    def incoming_connection(self, address: str) -> None:
        self.__signals.incoming_connection.emit(address)

    def accept_connection(self) -> None:
        self.__model.accept_connection()

    def decline_connection(self) -> None:
        self.__model.decline_connection()
