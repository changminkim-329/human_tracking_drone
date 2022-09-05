import socket
import threading
import time
import platform
import numpy as np
import matplotlib.pyplot as plt
import cv2


class Tello:
    def __init__(self):
        self.ip = '192.168.10.1'
        self.command_port = 8889
        self.address = (self.ip, self.command_port)
        self.response = None
        self.overtime = 3

        self.lock = threading.RLock()

        self.video_port = 11111

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        self.socket.bind(('0.0.0.0', self.command_port))

        # init command and video stream

        self.receive_thread = threading.Thread(target=self.receive_response)
        self.receive_thread.daemon = True

        self.socket.sendto(b'command', self.address)
        self.socket.sendto(b'battery?', self.address)
        print('sent: command')
        self.socket.sendto(b'streamoff', self.address)
        self.receive_thread.start()

        print("video start")



    def receive_response(self):
        while True:

            self.response, ip = self.socket.recvfrom(3000)
            print("msg receive")
            if self.response:
                print(str(self.response))


    def send_command(self, command):
        self.socket.sendto(command.encode('utf-8'), self.address)

    # control command:

    def takeoff(self):
        self.send_command('takeoff')

    def land(self):
        self.send_command('land')

    def streamon(self):
        self.send_command('streamon')

    def streamoff(self):
        self.send_command('streamoff')

    def end(self):
        self.send_command('end')

def receive_video_data():
    print('sent: streamon')
    try:
        while True:

            try:
                frame = cap.read()[1]


                cv2.imshow('frame',frame)

                if cv2.waitKey(22) & 0xFF == ord('q'):
                    break




            except Exception as e:
                print(e)
                continue



    except Exception as e:
        print("error")

starttime = time.clock()
print("wait...")
drone = Tello()
drone.streamon()
cap = cv2.VideoCapture('udp://@0.0.0.0:11111',cv2.CAP_FFMPEG)
print(time.clock()-starttime)

# video stream

"""
receive_video_thread = threading.Thread(target=receive_video_data)
receive_video_thread.daemon = True

receive_video_thread.start()
"""
print("15 second wait please")

while True:
    try:
        frame = cap.grab()

        frame = cap.retrieve()[1]
        cv2.imshow('frame', frame)

        if cv2.waitKey(22) & 0xFF == ord('q'):
            drone.streamoff()
            drone.end()
            drone.socket.close()
            cap.release()
            break



    except KeyboardInterrupt:
        print('\n . . .\n')
        drone.streamoff()
        drone.end()
        drone.socket.close()
        cap.release()

        break
