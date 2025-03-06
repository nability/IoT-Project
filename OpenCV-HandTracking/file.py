import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time

# Inisialisasi komunikasi serial dengan Arduino (sesuaikan dengan port Anda)
arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Tunggu koneksi serial stabil

detector = HandDetector(detectionCon=0.8, maxHands=1)

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    hands, img = detector.findHands(frame)
    
    if hands:
        lmlst = hands[0]
        fingerUp = detector.fingersUp(lmlst)
        print(fingerUp)
        
        # Kirim data ke Arduino berdasarkan jumlah jari yang terangkat
        if fingerUp == [0, 0, 0, 0, 0]:
            arduino.write(b'0')  # Semua LED mati
        elif fingerUp == [0, 1, 0, 0, 0]:
            arduino.write(b'1')  # LED 1 nyala
        elif fingerUp == [0, 1, 1, 0, 0]:
            arduino.write(b'2')  # LED 2 nyala
        elif fingerUp == [0, 1, 1, 1, 0]:
            arduino.write(b'3')  # LED 3 nyala
        elif fingerUp == [0, 1, 1, 1, 1]:
            arduino.write(b'4')  # LED 4 nyala
        elif fingerUp == [1, 1, 1, 1, 1]:
            arduino.write(b'5')  # Semua LED nyala
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
arduino.close()
