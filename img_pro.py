import os,sys
import cv2
from sqlalchemy import false, true
import serial
import time

#動画をとる
cap = cv2.VideoCapture(0)
#顔認識、目の認識
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

#ウィンク回数を数える変数count
count = 0

#片目開いているか否かのブーリアン
temp_side = false
#両目開いているかのブーリアン
temp_both = false

#Arduinoと接続
print("Open Port")
ser =serial.Serial("COM6", 9600) #COMポートはそれぞれの環境ごとに設定する

#OpenCVで動画からフレームごとに処理実行
while True:
    ret, rgb = cap.read()
    
    #顔認識
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(
        gray, scaleFactor=1.11, minNeighbors=3, minSize=(100, 100))

    #顔があれば
    if len(faces) == 1:
        x, y, w, h = faces[0, :]

        # 処理高速化のため顔の上半分を検出対象範囲とする
        eyes_gray = gray[y : y + int(h/2), x : x + w]
        eyes = eye_cascade.detectMultiScale(
            eyes_gray, scaleFactor=1.11, minNeighbors=3, minSize=(8, 8))

        #目の周りにバインディングボックス表示
        for ex, ey, ew, eh in eyes:
            cv2.rectangle(rgb, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 255, 0), 1)

        #両目開いている時
        if len(eyes) == 2:
            temp_both = true
            temp_side = false

        #片目の時
        if len(eyes) == 1:
            
            #1フレーム前（テンポラル変数）が両目だった時ウィンク判定
            if temp_both == true:
                count += 1

            #テンポラル変数更新
            temp_both = false
            temp_side = true
        
        #10回ウィンクできたら"reached 10!"と表示
        if count == 10:
            cv2.putText(rgb, 'reached 10!',
                (100,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,100,255), 2, cv2.LINE_AA)
            
            #Arduinoに書き込み
            ser.write("1".encode())

    cv2.putText(rgb, f'wink count {count}',
                (100,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,100,255), 2, cv2.LINE_AA)

    cv2.imshow('frame', rgb)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

#COMポート閉じる        
print("Close Port")
ser.close()


cap.release()
cv2.destroyAllWindows()
