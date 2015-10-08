import sys
import socket

from PyQt4.QtGui import QApplication, QTableWidget, QTableWidgetItem
from PyQt4.QtGui import QGridLayout, QLineEdit, QWidget, QHeaderView, QTextEdit

# Definition of HostInput class
# General description of what a 'HostInput' is
class HostInput(QLineEdit):
    def __init__(self, client):
        super(HostInput, self).__init__()
        self.client = client
        self.setText("Host Address")
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        self.client.host = str(self.text())
        print(self.client.host)

# Definition of PortInput class
# General description of what a 'PortInput' is
class PortInput(QLineEdit):
    def __init__(self, client):
        super(PortInput, self).__init__()
        self.client = client
        self.setText("Port")
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        self.client.port = int(self.text())
        print(self.client.port)
        self.client.connect()
        # Use the host and port to connect to the chat server
        
# Definition of TextBox class
# General description of what a 'TextBox' is
class TextBox(QLineEdit):
    def __init__(self, client):
        super(TextBox, self).__init__()
        self.client = client
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        self.client.msg_text = self.text()
        print(self.client.msg_text)

        # Send out the message to the server
        self.client.send_message()

        # Clear the message from the input box
        #self.setText("")
        
# Definition of ChatBox class
# General description of what a 'ChatBox' is
class ChatBox(QTextEdit):
    def __init__(self):
        super(ChatBox, self).__init__()

class ChatClient():
    def __init__(self, chat_box):
        self.chat_box = chat_box
        self.host = ""
        self.port = 0
        self.msg_text = ""
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print("Connecting to "+str(self.host)+":"+str(self.port))
        self.connection.connect((self.host, self.port))

    def send_message(self):
        print("Sending message: "+str(self.msg_text))
        self.connection.send(self.msg_text)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    chat_box = ChatBox()
    client = ChatClient(chat_box)   

    host_input = HostInput(client)
    port_input = PortInput(client)    
    text_box = TextBox(client)

    grid = QGridLayout()
    grid.addWidget(host_input, 1, 0)
    grid.addWidget(port_input, 1, 1)
    grid.addWidget(text_box, 2, 0, 1, 2)
    grid.addWidget(chat_box, 3, 0, 5, 2)

    main_frame = QWidget()
    main_frame.setLayout(grid)
    main_frame.show()

    # Wait to connect until we have a host and a port
    print("Waiting to connect")

    sys.exit(app.exec_())
