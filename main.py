from ultralytics import YOLO
import serial
import cv2
import pygame
import time

pygame.init()
model = YOLO('yolov8n.pt')
ultrasonic_data = serial.Serial('COM3', 9600)
cap = cv2.VideoCapture(0)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()
    z=model.predict(frame, show=True,classes=[0])
    # 0 is the class for human and 56 is for chair.
    x = ultrasonic_data.readline()
    val = str(x.decode().strip())
    dist = int(val)
    cv2.imshow("image0.jpg", frame)
    if(dist>500):
        print("Detecting Distance....")
        cv2.rectangle(frame, (10, 10), (300, 50), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, "Detecting", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif(dist>200 and dist<=500 ):
        print("Distance: ",dist)
        cv2.rectangle(frame, (10, 10), (300, 50), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, "Safe Distance", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif(dist>100 and dist<=200):
        print("Distance: ",dist," Close-> Inside layer 1")
        sound_file = 'warning.mp3'
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        time.sleep(1)
        cv2.rectangle(frame, (10, 10), (200, 50), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, "Close", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif(dist<=100):
        print("Distance: ", dist, " Very Close-> Inside layer 2, Turn off machine")
        cv2.rectangle(frame, (10, 10), (300, 50), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, "Very Close", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        sound_file = 'alert.mp3'
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        time.sleep(1)
    cv2.imshow("image0.jpg", frame)

cap.release()
cv2.destroyAllWindows()
