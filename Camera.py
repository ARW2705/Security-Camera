import picamera
import time

class SecurityCamera:

    def __init__(self, vflip=True, hflip=True, resolution=(1280, 720),
                 framerate=24, rotation=0, format='h264'):
        self.camera = picamera.PiCamera()
        self.camera.led = False
        self.max_duration = 3600
        self.is_recording = False
        self.camera.vflip = vflip
        self.camera.hflip = hflip
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.rotation = rotation
        self.format = format

    def set_camera_options(self, options):
        for key, value in options.iteritems():
            setattr(self.camera, key, value)

    def start_recording(self, connection):
        if self.is_recording or not connection:
            return
        self.is_recording = True
        self.camera.start_preview()
        time.sleep(2)
        print('Start recording')
        self.camera.start_recording(connection, format=self.format)

    def recording(self):
        while self.is_recording:
            self.camera.wait_recording(1)
        return

    def stop_recording(self):
        if self.is_recording:
            print('Stop recording')
            self.camera.stop_recording()
            self.is_recording = False
