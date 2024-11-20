import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
import telegram
from yolo import Yolo_Detect
from datetime import datetime
import asyncio


# call class Yolo_Detect and object_detection methods
# if draw values=0, false values =1
detector = Yolo_Detect("home_cam.mp4", 1)
detector.setup_mouse_callback()
detector.object_detection()
