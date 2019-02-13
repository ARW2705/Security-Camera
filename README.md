# Home Security Camera

Work in Progress

This application provides a client setup in which a
raspberry pi compatible camera can stream video to a
python server via a TCP socket and communicate with
a messaging server via socket.io

## Hardware

* Raspberry Pi Zero-W
* Raspberry Pi compatible power supply
* Arducam 5 MP camera
* Arducam CSI to HDMI cable extension module
* PIR motion sensor

## Usage

By default, motion detection is enabled and will begin
camera recording on activation. The user may also begin
recording via the messaging socket.

## Future plans

* Enable live streaming on demand
* Send notification on motion sensor trigger
* Add additional cameras

## Author

Andrew Wanex

## License
[MIT](https://github.com/ARW2705/Security-Camera/blob/master/LICENSE)
