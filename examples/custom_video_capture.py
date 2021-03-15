import cv2
import numpy as np
from webrtc_streaming import start_streaming

"""
    Connect to signaling server and wait for viewers who know the secret key
    MyOwnVideoCapture generates an white noise streaming.

    Usage:
        python custom_video_capture.py
"""

SECRET_KEY = "TEST_NOISE"


class MyOwnVideoCapture:
    def __init__(self):
        pass

    def read(self):
        return True, np.random.randint(
            255, size=(720, 1280, 3), dtype=np.uint8)


start_streaming(signaling_server="https://bluearas.cloud",
                path="webrtc_socket",
                secret_key=SECRET_KEY,
                video_capture=cv2.VideoCapture("tcp://192.168.100.203:11112"),
                img_size=(256, 144))
