# %%
import cv2
import face_recognition
#import numpy as np
#from picamera import PiCamera

# %%
#from matplotlib import pyplot as plt
#GIOP用のモジュールと時間制御用のモジュールをインポート
import RPi.GPIO as GPIO
import time

# %%

#camera = PiCamera()

# %%
#画像を取得する
known_face_imgs = []
for path in ["../Biden.jpg", "../Elon.jpg", "../Messi.jpg", "../Trump.jpg"]:
    image = face_recognition.load_image_file(path)
    known_face_imgs.append(image)
#known_image = face_recognition.load_image_file("../Messi.jpg")

#それぞれの顔画像から特徴を抽出する
known_face_encodings = []
for known_face_img in known_face_imgs:
    encod = face_recognition.face_encodings(known_face_img)[0]
    known_face_encodings.append(encod)
#messi_encoding = face_recognition.face_encodings(known_image)[0]

known_face_names = ["Biden", "Elon", "Messi", "Trump"]
#ぞれぞれの顔画像の特徴を比較する

#results = face_recognition.compare_faces([messi_encoding], unknown_encoding)
#print(results)

# %%
#認識した顔のを線で囲み、名前を表示する
#def draw_face_locations(img, locations, n):
    #fig, ax = plt.subplots()
    #ax.imshow(img)
    #ax.set_axis_off()


    #for i, (top, right, bottom, left) in zip(n, locations):
        # 長方形を描画する。
      
        #w, h = right - left, bottom - top
        #ax.add_patch(plt.Rectangle((left, top), w, h, ec="r", lw=2, fill=None))
        #ax.text(left, top,i)
    #plt.show()

def boxes(img, locations, n):
    for i, (top,right,bottom,left) in zip(n, locations):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(img, (left, top), (right, bottom), (0,0,255), 2)
        cv2.rectangle(img, (left,bottom-35), (right, bottom), (0,0,255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, i, (left + 6, bottom - 6), font, 1.0, (255,255,255),1)
    cv2.imshow('Video', img)
    #print("cv2 imshow")
    return
    

# %%
video_capture = cv2.VideoCapture(0)

while True:
    #frame = camera.start_preview()
    ret, frame = video_capture.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    #rgb_small_frame = small_frame[:,:,::-1]
    
    #unknown_image = face_recognition.load_image_file("../unknown3.jpg")
    face_locations = face_recognition.face_locations(small_frame)
    print(len(face_locations))
    #print(len(face_locations))
    unknown_encodings = face_recognition.face_encodings(small_frame, face_locations)
    #print(len(unknown_encodings))

    #結果を表示する
    #print(face_locations)
    face_names = []
    for unknown_encoding in unknown_encodings:
        result = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
        
        #print(result)
        if True in result:

            first_match = result.index(True)
            name = known_face_names[first_match]
            # %%
            

            #ポート番号を定義
            gp_out = 4
            #GPIOの設定
            GPIO.setmode(GPIO.BCM)  #GPIOのモードをGPIO.BCMに設定
            GPIO.setup(gp_out, GPIO.OUT)    #GPIO4を出力モードに設定

            #PWMの設定
            #サーボモータSG90の周波数は、50Hz 
            servo = GPIO.PWM(gp_out, 50)
            servo.start(0)

            servo.ChangeDutyCycle(2.5)
            time.sleep(5)

            servo.ChangeDutyCycle(7.25)
            time.sleep(0.5)

            servo.stop()
            GPIO.cleanup()



            #face_location = face_locations
        else:
            name = "unknown"
        face_names.append(name)
        
    boxes(frame, face_locations, face_names)
    
    #draw_face_locations(frame, face_locations, face_names)
    #if plt.waitforbuttonpress():
    
    if cv2.waitKey(1) != -1:
        print("key pressed")
        break

video_capture.release()
cv2.destroyAllWindows()
#camera.stop_preview()

# %%
