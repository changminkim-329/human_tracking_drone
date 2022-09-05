import socket
import threading
import time
import platform
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras as tk
from tensorflow.keras.models import model_from_json

from utils import WeightReader, decode_netout, draw_boxes
import cv2

import detector_setting as set

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

        self.frame = None

        # video detectipon thread

        self.video_detector_thread = threading.Thread(target=self.video_detector)
        self.video_detector_thread.daemon = True

        # self.receive_video_thread.start()



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

    def video_detector(self):
        json_file = open("./model/yolov2_model.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("./model/yolov2_weight.h5")

        try:
            while True:

                try:
                    if self.frame!=None:
                        prec_image = cv2.resize(self.frame, (416, 416)).astype('float32')
                        prec_image = prec_image / 255.0

                        image_predict = loaded_model.predict(np.expand_dims(prec_image, axis=0))


                        boxes = decode_netout(image_predict[0],
                                              obj_threshold=set.OBJ_THRESHOLD,
                                              nms_threshold=set.NMS_THRESHOLD,
                                              anchors=set.ANCHORS,
                                              nb_class=set.CLASS)

                        box_image = draw_boxes(self.frame, boxes, labels=set.LABELS)

                        self.frame = box_image.astype('int32')

                except Exception as e:
                    print(e)
                    continue


        except Exception as e:
            print("error")

print("wait...")
drone = Tello()
drone.streamon()
cap = cv2.VideoCapture('udp://@0.0.0.0:11111',cv2.CAP_FFMPEG)


print("15 second wait please")

while True:
    try:
        frame = cap.grab()

        frame = cap.retrieve()[1]

        drone.frame = frame
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
