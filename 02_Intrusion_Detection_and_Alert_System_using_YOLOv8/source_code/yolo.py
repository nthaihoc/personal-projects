import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
import telegram
from datetime import datetime
import pytz
import asyncio

class Yolo_Detect:
    def __init__ (self, file_video, select):
        self.file_model           = YOLO("runs/detect/train/weights/best.pt")
        self.file_video           = file_video
        self.thes                 = 0.5
        self.count                = 0
        self.last_alert           = None
        self.alert_telegram_each  = 10
        self.model                = YOLO("yolov8n.pt")
        self.config_data          = "config.yaml"
        self.select               = select
    def train_model(self, number):
        train_yolo = self.model
        result = train_yolo.train(data=self.config_data, epochs=number)

    async def send_telegram(self):
        self.photo_path = "alert.png"
        try:
            my_token = "6797495187:AAGXZ35qwDB4BlHVZ83ugTpS2jUwWXRHXQI"
            bot = telegram.Bot(token=my_token)
            await bot.sendPhoto(chat_id="5143772247", photo=open(self.photo_path, "rb"), caption="Phát hiện người xâm nhập !!!")
        except Exception as ex:
            print("Không thể gửi tin nhắn tới telegram ", ex)

        print("Gửi thành công")

    def warning(self, image):
        cv2.putText(image, "CANH BAO !!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if (self.last_alert is None) or (
                (datetime.now(pytz.utc) - self.last_alert).total_seconds() > self.alert_telegram_each):
            self.last_alert = datetime.now(pytz.utc)
            cv2.imwrite("alert.png", cv2.resize(image, dsize=None, fx=0.5, fy=0.5))
            asyncio.run(self.send_telegram())
        return image
    
    def RGB(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            point = [x, y]
            print(point)

    def setup_mouse_callback(self):
        cv2.namedWindow('Object Detection')
        cv2.setMouseCallback('Object Detection', self.RGB)

    def object_detection(self):
        cap = cv2.VideoCapture(self.file_video)
        area = [(24, 423), (578, 226), (641, 264), (45, 477)]
        while True:
            ret, self.frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            self.count += 1
            if self.count % 3 != 0:
                continue
            results = self.file_model.predict(self.frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")

            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                score = row[4]
                d = int(row[5])
                cx=int(x1+x2)//2
                cy=int(y1+y2)//2
                w, h = x2-x1, y2-y1
                cv2.polylines(self.frame,[np.array(area,np.int32)],True,(0,0,255),2)
                ob = cv2.pointPolygonTest(np.array(area, np.int32), ((cx, cy)), False)
                if ob > 0:
                    if score > self.thes:
                        print("ob =", ob)
                        print("Phát hiện xâm nhập")
                        cvzone.cornerRect(self.frame, (x1, y1, w, h), 3, 2)
                        cv2.circle(self.frame,(cx,cy),4,(255,0,0),-1)
                        cvzone.putTextRect(self.frame, f"person", (x1, y1), 1, 1)
                        self.warning(image=self.frame)
                        
            cv2.imshow("Object Detection", self.frame) #cv2.resize(self.frame, (640, 360))
            if cv2.waitKey(self.select)&0xFF==27:
                break
        cap.release()
        cv2.destroyAllWindows()

        
        