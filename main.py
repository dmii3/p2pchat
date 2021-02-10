from src.model.p2pchat import P2PChat
from src.model.states.factory import StateFactory
from src.view.mainwindow import MainWindow
from src.controller.mainwindowcontroller import MainWindowController
import argparse


from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='port for incoming connections')
    a = parser.parse_args()
    app = QApplication()
    model = P2PChat(StateFactory(), int(a.port))
    view = MainWindow()
    controller = MainWindowController(model, view)
    view.show()

    exit(app.exec_())



# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--port', help='port for incoming connections')
#     a = parser.parse_args()
#     factory = StateFactory()
#     chat = P2PChat(factory, inbound_port=int(a.port))
#
#     try:
#         while True:
#             user_input = input()
#             if user_input.startswith('/'):
#                 command_args = user_input.split(' ')
#                 command = command_args[0].upper()
#                 if command == "/C":
#                     if len(command_args) < 3:
#                         host = input("Enter destination address: ")
#                         port = int(input("Enter destination port: "))
#                         # host, port = 'localhost', 8888
#                     else:
#                         host, port = command_args[1], int(command_args[2])
#                     chat.connect_to(host, port)
#                 elif command == "/ACCEPT":
#                     chat.accept_connection()
#                 elif command == "/DECLINE":
#                     chat.decline_connection()
#                 elif command == "/DISCONNECT":
#                     chat.disconnect()
#                 elif command == "/EXIT":
#                     chat.exit()
#                     break
#             else:
#                 chat.send_message(user_input)
#     except KeyboardInterrupt:
#         chat.exit()
