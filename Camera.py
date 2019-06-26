import picamera
import time

class SecurityCamera:
    '''
    PiCamera system in use with Arducam camera module

    @attr: camera            (PiCamera)        - PiCamera instance
    @attr: camera.led        (bool)            - red LED on Arducam
    @attr: max_duration      (int)             - maximum recording duration in seconds
    @attr: is_recording      (bool)            - true if camera has called start_recording()
    @attr: camera.vflip      (bool)            - flip vertical axis of camera
    @attr: camera.hflip      (bool)            - flip horizontal axis of camera
    @attr: camera.resolution (tuple(int, int)) - recording resolution in pixels (horizontal, vertical)
    @attr: camera.framerate  (int)             - framerate to record
    @attr: camera.rotation   (int)             - image rotation of camera in degrees
    @attr: format            (str)             - recording file type
    '''

    def __init__(self, vflip=True, hflip=True, resolution=(1280, 720),
                 framerate=24, rotation=0, format='h264'):
        self.camera = picamera.PiCamera()
        self.camera.led = False # turn red LED off by default
        self.max_duration = 3600
        self.is_recording = False
        self.camera.vflip = vflip
        self.camera.hflip = hflip
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.rotation = rotation
        self.format = format

    def set_camera_options(self, options):
        '''
        Map camera settings - unknown settings are ignored

        @params: options (dict(str, any)) - key, value pairs of camera settings
        '''
        for key, value in options.iteritems():
            if hasattr(self.camera, key):
                setattr(self.camera, key, value)

    def start_recording(self, connection):
        '''
        Start PiCamera recording

        @params: connection (StreamSocket) - tcp streaming socket
        '''
        if self.is_recording or not connection:
            return
        self.is_recording = True
        self.camera.start_preview()
        time.sleep(2) # sleep 2s to allow camera to prepare for recording
        print('Start recording')
        self.camera.start_recording(connection, format=self.format)

    # TODO: determine if wait_recording() should be a separate thread
    def recording(self):
        while self.is_recording:
            self.camera.wait_recording(1) # allows error detection during recording
        return

    def stop_recording(self):
        if self.is_recording:
            print('Stop recording')
            self.camera.stop_recording()
            self.is_recording = False
