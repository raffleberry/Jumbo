import time
import pygame
from pydarknet import Detector, Image
import cv2
import threading
import requests
import json
from twilio.rest import Client

pygame.mixer.init(44100, -16,2,2048)
s = pygame.mixer.Sound('bee.wav')

sent = 0

def sendSMS():
    account_sid = 'ACd6687526ddd249e5dd9a731ee20a05fc'
    auth_token = '6f3a73235618d67768a97e4658b5acf5'
    client = Client(account_sid, auth_token)

    nums = ['+917684085576','+918895688875','+918763323038','+919438017057']

    for num in nums:
        message = client.messages.create(
                                  from_='+17275132450',
                                  body='Elephant Detected at camera 1',
                                  to=num
                              )
        print(message.sid)
    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic ZTA0YmUzNTEtM2QxNy00ODY3LWI2ZWEtYzQ0MGVhZDRmYTNh"}

    payload = {"app_id": "ebf6c722-f187-4a16-a758-47c09f588d71",
               "included_segments": ["All"],
               "contents": {"en": "ALERT!!! Elephant Detected"}}
     
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

    print(req.status_code, req.reason)

def go():
    s.play()

sms = 0

if __name__ == "__main__":
    # Optional statement to configure preferred GPU. Available only in GPU version.
    # pydarknet.set_cuda_device(0)

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    cap = cv2.VideoCapture(0)
#    cap = cv2.VideoCapture('http://192.168.43.88:8080/stream.mjpeg')
    while True:
        r, frame = cap.read()
        if r:
            #start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame)
            results = net.detect(dark_frame)
            del dark_frame

            #end_time = time.time()
            #print("Elapsed Time:",end_time-start_time)

            for cat, score, bounds in results:
                x, y, w, h = bounds
                cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(0,255,0))
                who = str(cat.decode("utf-8"))
                if who.lower() == "elephant":
                  threading.Thread(target=go).start()
                  #print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nELEPHANT!!!!!!\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                  if (sent == 0):
                      sent = 1
                      threading.Thread(target=sendSMS).start()

                cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 153, 51))

            cv2.imshow("preview", frame)

        k = cv2.waitKey(1)
        if k == 0xFF & ord("q"):
            break
