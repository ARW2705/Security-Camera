import time
from threading import Thread, Timer

import RPi.GPIO as GPIO

class MotionDetection(Thread):
    '''
    PIR Motion Detection hardware interface

    @attr: motion_detected (bool)   - true if motion has been detected
    @attr: run_detection   (bool)   - true to run detection loop
    @attr: thread          (Thread) - motion detection parallel thread daemon
    @attr: thread.daemon   (bool)   - true to end thread on program exit
    '''
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.motion_detected = False
        self.run_detection = False
        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def begin_detection(self):
        self.run_detection = True

    def end_detection(self):
        self.run_detection = False

    def run(self):
        '''
        Motion detection daemon
        '''
        try:
            while True:
                # main motion detection loop
                if self.run_detection and GPIO is not None:
                    i = GPIO.input(4)
                    self.motion_detected = bool(i)
                    if (self.motion_detected):
                        time.sleep(5) # allow 5s time gap from last motion detected
                    else:
                        time.sleep(0.5)

        except TypeError, e:
            print('Motion error: {}'.format(e))
            print(e.message)
            print(e.args)
