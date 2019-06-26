import socket

class StreamSocket():
    '''
    Camera streaming tcp socket

    @attr: ip_addr             (str)         - ip address for streaming tcp connection
    @attr: port                (int)         - port number for streaming tcp connection
    @attr: client              (socket)      - tcp socket connection
    @attr: is_connected        (bool)        - true if tcp socket is connected
    @attr: connection          (file_object) - tcp socket connection file like object
    @attr: BUFSIZE             (int)         - tcp buffer size in bytes
    @attr: is_stream_requested (bool)        - true if streaming socket has been connected
    '''
    def __init__(self, ip_addr='192.168.0.110', port=3030):
        self.ip_addr = ip_addr
        self.port = port
        self.client = None
        self.is_connected = False
        self.connection = None
        self.BUFSIZE = 4096
        self.is_stream_requested = False

    def connect(self):
        '''
        Create simple socket tcp connection
        '''
        try:
            if self.client is None:
                print('Streaming socket connected to {} on port {}'.format(self.ip_addr, self.port))
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.is_connected = True
                self.is_stream_requested = True
        except (socket.error), exception:
            print(exception)

    def reconnect(self):
        '''
        Automatically try to reconnect if connection is broken, but stream is requested
        '''
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
        '''
        Create file like object from tcp connection
        '''
        if self.connection is None:
            self.client.connect((self.ip_addr, self.port))
            self.connection = self.client.makefile('wb')
