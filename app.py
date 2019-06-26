#!/usr/bin/env python

import traceback
import sys
import subprocess

from StreamSocket import StreamSocket
from MessageSocket import MessageSocket
from Camera import SecurityCamera
from MotionDetection import MotionDetection
from CableException import CableDisconnectedException

def handle_message(message, sock=None, cam=None, detector=None):
    '''
        Handle incoming tcp socket messages

        @params: message  (dict(str, any))  - incoming tcp socket message as key, value pair
        @params: sock     (MessageSocket)   - messaging tcp socket instance
        @params: cam      (PiCamera)        - PiCamera camera instance
        @params: detector (MotionDetection) - GPIO MotionSensor detector instance
    '''

    # Each message will have a single key, value pair
    title = message.keys()[0]
    body = message.values()[0]

    try:
        if title == 'set-camera': # body contains key, value pairs of camera settings
            cam.set_camera_options(body)
        elif title == 'stream': # body is boolean to toggle user requested camera activation
            sock.request_stream = body
        elif title == 'motion-detection': # body is boolean to toggle motion detection on/off
            detector.run_detection = body
        elif title == 'shutdown': # body will be empty
            sock.request_exit = True # will end main app loop
        else:
            raise ValueError('Payload title "{}" is not valid'.format(payload.title))
        sock.pop_message()
    except (ValueError, AttributeError) as exception:
        print('Message handling exception: {}'.format(exception))

def is_HDMI_connected():
    # Check if the HDMI cable has been disconnected
    return '1' == subprocess.check_output(['vcgencmd', 'get_camera'])[0:-1].split(' ')[1][-1]

def main():
    stream_socket = StreamSocket() # video streaming only tcp connection
    message_socket = MessageSocket() # command message only tcp connection
    cam = SecurityCamera()
    detector = MotionDetection()

    message_socket.connect()
    detector.begin_detection() # activate motion detection by default

    try:
        print('Starting Picamera loop')
        # main loop
        while not message_socket.request_exit:
            if not is_HDMI_connected():
                # exit to prevent outside access if someone disconnects the HDMI
                # between the camera module and RPi
                raise CableDisconnectedException()

            if len(message_socket.messages):
                # a message is waiting to be processed
                handle_message(message_socket.messages[0], message_socket, cam, detector)

            if detector.motion_detected or message_socket.request_stream:
                '''
                    camera activation was triggered by motion detection or user input
                    open stream socket, begin camera recording, and send feedback
                    message regarding what event triggered the camera activation
                '''
                stream_socket.connect()
                stream_socket.create_connection() # create file like connection for camera
                message_socket.notify_trigger_event(detector.motion_detected, message_socket.request_stream)
                cam.start_recording(stream_socket.connection)

            if not detector.motion_detected and not message_socket.request_stream:
                if cam.is_recording:
                    cam.stop_recording()
                    stream_socket.disconnect()
                    message_socket.is_notification_sent = False

    except (KeyboardInterrupt, CableDisconnectedException), exception:
        print('Terminating due to: {}'.format(sys.exc_info()[0]))

    except:
        print('Unknown error in main: {}'.format(sys.exc_info()[0]))
        print(sys.exc_info())
        tb = traceback.format_exc()
        print(tb)

    finally:
        print('Quitting')
        cam.stop_recording()
        stream_socket.disconnect()
        sys.exit()

if __name__ == '__main__':
    main()
