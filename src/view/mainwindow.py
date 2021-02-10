from __future__ import annotations

from PySide2.QtWidgets import QPushButton, QHBoxLayout, QWidget, QGridLayout, QLineEdit, QLabel, QTextEdit, QMessageBox
from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtGui import QCloseEvent, QKeyEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controller.mainwindowcontroller import MainWindowController


class CustomTextEdit(QTextEdit):
    enter_pressed = Signal(str)

    def __init__(self):
        QTextEdit.__init__(self)
        self.prev_key = None

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            if self.prev_key == Qt.Key_Shift:
                self.append('')
                return
            elif self.toPlainText() != '':
                self.enter_pressed.emit(self.toPlainText())
        else:
            self.prev_key = e.key()
            super().keyPressEvent(e)


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.__init_ui()
        self.__controller = None  # type: MainWindowController

        self.push_button_connect.clicked.connect(
            lambda: self.__controller.connect_clicked(self.line_edit_host.text(), self.line_edit_port.text())
        )
        # self.push_button_settings.clicked.connect(self.controller.settings_clicked)
        self.push_button_send.clicked.connect(
            lambda: self.__controller.send_clicked(self.text_edit_new_message.toPlainText())
        )
        self.text_edit_new_message.enter_pressed.connect(
            lambda: self.__controller.send_clicked(self.text_edit_new_message.toPlainText())
        )

    def __init_ui(self) -> None:
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWindowTitle(u"P2P Chat")
        layout = QGridLayout()
        self.setLayout(layout)

        self.label_your_address = QLabel(u"Your address: ")
        layout.addWidget(self.label_your_address, 0, 0, Qt.AlignLeft)

        hor_layout = QHBoxLayout()

        label_host = QLabel(u"Host")
        hor_layout.addWidget(label_host)

        self.line_edit_host = QLineEdit()
        hor_layout.addWidget(self.line_edit_host)

        label_port = QLabel(u"Port")
        hor_layout.addWidget(label_port)

        self.line_edit_port = QLineEdit()
        self.line_edit_port.setMaximumWidth(45)
        self.line_edit_port.setAlignment(Qt.AlignCenter)
        hor_layout.addWidget(self.line_edit_port)

        self.push_button_connect = QPushButton(u"Connect")
        hor_layout.addWidget(self.push_button_connect)

        self.push_button_settings = QPushButton(u"⚙")
        f = self.push_button_settings.font()
        f.setPointSize(15)
        self.push_button_settings.setMaximumHeight(25)
        self.push_button_settings.setMaximumWidth(25)
        self.push_button_settings.setFont(f)

        hor_layout.addWidget(self.push_button_settings)

        layout.addLayout(hor_layout, 1, 0)

        self.text_edit_message_history = QTextEdit()
        self.text_edit_message_history.setAcceptRichText(False)
        self.text_edit_message_history.setReadOnly(True)
        layout.addWidget(self.text_edit_message_history, 2, 0)

        new_mes_layout = QHBoxLayout()

        self.text_edit_new_message = CustomTextEdit()
        self.text_edit_new_message.setAcceptRichText(False)
        self.text_edit_new_message.setMaximumHeight(70)
        new_mes_layout.addWidget(self.text_edit_new_message)

        self.push_button_send = QPushButton(u"Send")
        self.push_button_send.setMaximumHeight(70)
        new_mes_layout.addWidget(self.push_button_send)
        layout.addLayout(new_mes_layout, 4, 0)

    def set_controller(self, controller: MainWindowController) -> None:
        self.__controller = controller

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__controller.form_closed()
        super().closeEvent(event)

    @Slot(str)
    def show_message_box(self, text: str) -> None:
        QMessageBox.critical(self, "Error!", text)

    @Slot(str)
    def update_chat_history(self, new_message: str) -> None:
        self.text_edit_message_history.append(new_message)

    @Slot(str)
    def show_connection_dialog(self, address: str) -> None:
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Incoming connection")
        dialog.setText(f"Connection from {address}. Accept?")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.Yes)
        ret = dialog.exec_()
        if ret == QMessageBox.Yes:
            self.__controller.accept_connection()
        elif ret == QMessageBox.No:
            self.__controller.decline_connection()
