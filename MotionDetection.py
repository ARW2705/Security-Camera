import time
from threading import Thread, Timer

import RPi.GPIO as GPIO

class MotionDetection(Thread):
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
        try:
            while True:
                if self.run_detection and GPIO is not None:
                    i = GPIO.input(4)
                    self.motion_detected = bool(i)
                    if (self.motion_detected):
                        time.sleep(5)
                    else:
                        time.sleep(0.5)

        except TypeError, e:
            print('Motion error: {}'.format(e))
            print(e.message)
            print(e.args)

