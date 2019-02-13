import socket

class StreamSocket():
    def __init__(self, ip_addr='192.168.0.110', port=3030):
        self.ip_addr = ip_addr
        self.port = port
        self.client = None
        self.is_connected = False
        self.connection = None
        self.BUFSIZE = 4096
        self.is_stream_requested = False

    def connect(self):
        try:
            if self.client is None:
                print('Streaming socket connected to {} on port {}'.format(self.ip_addr, self.port))
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.is_connected = True
                self.is_stream_requested = True
        except (socket.error), exception:
            print(exception)

    def reconnect(self):
        if self.is_stream_requested and not self.is_connected:
            self.client.close()
            self.client = None
            self.connect()

    def disconnect(self):
        if self.is_connected:
            self.client.close()
            self.client = None
            self.connection = None
            self.is_connected = False
            self.is_stream_requested = False

    def create_connection(self):
        if self.connection is None:
            self.client.connect((self.ip_addr, self.port))
            self.connection = self.client.makefile('wb')
