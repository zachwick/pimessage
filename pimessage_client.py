import sys
import socket

from PyQt4.QtGui import QApplication, QTableWidget, QTableWidgetItem
from PyQt4.QtGui import QGridLayout, QLineEdit, QWidget, QHeaderView, QTextEdit

# Definition of HostInput class
# General description of what a 'HostInput' is
class HostInput(QLineEdit):
    def __init__(self, chat):
        super(HostInput, self).__init__()
        self.host = ""
        self.chat = chat
        self.setText("Host Address")
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        self.host = self.text()
        print(self.host)

# Definition of PortInput class
# General description of what a 'PortInput' is
class PortInput(QLineEdit):
    def __init__(self, chat):
        super(PortInput, self).__init__()

        self.port = ""
        self.chat = chat
        self.setText("Port")
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        self.port = self.text()        
        print(self.port)
        # Use the host and port to connect to the chat server
        
# Definition of TextBox class
# General description of what a 'TextBox' is
class TextBox(QLineEdit):
    def __init__(self, chat):
        super(TextBox, self).__init__()
        self.msg_text = ""
        self.chat = chat
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        self.msg_text = self.text()
        print(self.msg_text)
        # Send out the message to the server
        
# Definition of ChatBox class
# General description of what a 'ChatBox' is
class ChatBox(QTextEdit):
    def __init__(self, chat):
        super(ChatBox, self).__init__()
        self.chat = chat

class ChatClient():
    def __init__(self, app, host, port, text_box, chat_box):
        self.app = app
        self.host = host
        self.port = port
        self.text_box = text_box
        self.chat_box = chat_box
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sys.exit(self.app.exec_())

    def connect(self):
        print("Connecting to "+self.host.host+":"+self.port.port)
        self.connection.connect((self.host.host, self.port.port))
        # while 1:
        #     data = client_socket.recv(512)
        #     if ( data == 'q' or data == 'Q'):
        #         client_socket.close()
        #         break;
        #     else:
        #         print "RECIEVED:" , data
        #         data = raw_input ( "SEND( TYPE q or Q to Quit):" )
        #         if (data <> 'Q' and data <> 'q'):
        #             client_socket.send(data)
        #         else:
        #             client_socket.send(data)
        #             client_socket.close()
        #             break;
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    chat = ""
    host_input = HostInput(chat)
    port_input = PortInput(chat)
    
    text_box = TextBox(chat)
    chat_box = ChatBox(chat)

    grid = QGridLayout()
    grid.addWidget(host_input, 1, 0)
    grid.addWidget(port_input, 1, 1)
    grid.addWidget(text_box, 2, 0, 1, 2)
    grid.addWidget(chat_box, 3, 0, 5, 2)

    main_frame = QWidget()
    main_frame.setLayout(grid)
    main_frame.show()

    client = ChatClient(app, host_input, port_input, text_box, chat_box)   
    # Wait to connect until we have a host and a port
    print("Waiting to connect")
