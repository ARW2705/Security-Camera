from threading import Thread
from socketIO_client_nexus import SocketIO, LoggingNamespace

class MessageSocket():
    '''
    Handles tcp socket command messaging

    @attr: ip_addr              (str)                  - string containing ip address for socket connection
    @attr: port                 (int)                  - tcp port for socket connection
    @attr: client               (SocketIO)             - socketIO client
    @attr: message              (list(dict(str, any))) - list of messages from socket
    @attr: thread               (Thread)               - thread daemon that the messaging socket operates from
    @attr: request_exit         (bool)                 - program exit request
    @attr: request_stream       (bool)                 - camera on/off request
    @attr: is_notification_sent (bool)                 - trigger notification was sent
    '''
    def __init__(self, ip_addr='192.168.0.110', port=3575):
        self.ip_addr = ip_addr
        self.port = port
        self.client = None
        self.messages = []
        self.thread = None
        self.request_exit = False
        self.request_stream = False
        self.is_notification_sent = False

    def connect(self):
        '''
        Start a daemon to run messaging socket in parallel that closes when program exits
        '''
        if self.client is None:
            self.thread = Thread(target=self.listen, args=())
            self.thread.daemon = True
            self.thread.start()

    def listen(self):
        '''
        Listen for incoming tcp messages and route to handler
        '''
        self.client = SocketIO(self.ip_addr, self.port, LoggingNamespace)
        self.client.on('echo-proxy-request-set-camera', self.on_request)
        self.client.on('echo-proxy-request-stream', self.on_request)
        self.client.on('echo-proxy-request-set-motion-detection', self.on_request)
        self.client.on('echo-proxy-request-shutdown', self.on_request)
        print('Message socket connected to {} on port {}'.format(self.ip_addr, self.port))
        self.client.wait()

    def on_request(self, *args):
        '''
        Add new request message to pending queue
        '''
        self.messages.append(args[0])

    def pop_message(self):
        '''
        Remove from front of queue
        '''
        self.messages.pop(0)

    def notify_trigger_event(self, motion=False, request=False):
        '''
        Emit feedback of camera activation
        '''
        if motion:
            event = 'motion'
        elif request:
            event = 'request'
        else:
            event = 'error'
        if not self.is_notification_sent:
            self.client.emit('response-new-video-trigger-event', {'triggerEvent': event})
            self.is_notification_sent = True
