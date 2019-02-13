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
    title = message.keys()[0]
    body = message.values()[0]

    try:
        if title == 'set-camera':
            cam.set_camera_options(body)
        elif title == 'stream':
            sock.request_stream = body
        elif title == 'motion-detection':
            detector.run_detection = body
        elif title == 'shutdown':
            sock.request_exit = True
        else:
            raise ValueError('Payload title "{}" is not valid'.format(payload.title))
        sock.pop_message()
    except (ValueError, AttributeError) as exception:
        print('Message handling exception: {}'.format(exception))

def is_HDMI_connected():
    return '1' == subprocess.check_output(['vcgencmd', 'get_camera'])[0:-1].split(' ')[1][-1]

def main():
    stream_socket = StreamSocket()
    message_socket = MessageSocket()
    cam = SecurityCamera()
    detector = MotionDetection()

    message_socket.connect()
    detector.begin_detection()

    try:
        print('Starting Picamera loop')
        # main loop
        while not message_socket.request_exit:
            if not is_HDMI_connected():
                raise CableDisconnectedException()

            if len(message_socket.messages):
                handle_message(message_socket.messages[0], message_socket, cam, detector)

            if detector.motion_detected or message_socket.request_stream:
                stream_socket.connect()
                stream_socket.create_connection()
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

