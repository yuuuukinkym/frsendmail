#opencvをインポートする
import cv2
#顔認証のためのモジュールをインポートする
import face_recognition
#GIOP用のモジュールと時間制御用のモジュールをインポート
import RPi.GPIO as GPIO
import time



#画像を取得する
known_face_imgs = []
for path in ["../Biden.jpg", "../Elon.jpg", "../Messi.jpg", "../Trump.jpg"]:
    image = face_recognition.load_image_file(path)
    #読み込んだ画像をリストに入れる
    known_face_imgs.append(image)

#それぞれの顔画像から特徴を抽出する
known_face_encodings = []
for known_face_img in known_face_imgs:
    encod = face_recognition.face_encodings(known_face_img)[0]
    known_face_encodings.append(encod)

#それぞれの画像の順番に名前のリストを作成
known_face_names = ["Biden", "Elon", "Messi", "Trump"]


#画像に顔の位置と名前を表示する関数
def boxes(img, locations, n):
    for i, (top,right,bottom,left) in zip(n, locations):
        #元の画像の大きさに戻す
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(img, (left, top), (right, bottom), (0,0,255), 2)
        cv2.rectangle(img, (left,bottom-35), (right, bottom), (0,0,255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, i, (left + 6, bottom - 6), font, 1.0, (255,255,255),1)
    cv2.imshow('Video', img)
    return
    

#ライブ映像を取得する
video_capture = cv2.VideoCapture(0)

#ポート番号を定義
gp_out = 4
#GPIOの設定
GPIO.setmode(GPIO.BCM)  #GPIOのモードをGPIO.BCMに設定
GPIO.setup(gp_out, GPIO.OUT)    #GPIO4を出力モードに設定
#PWMの設定
#サーボモータSG90の周波数は、50Hz
servo = GPIO.PWM(gp_out, 50)
servo.start(0)


while True:
    #画像処理を再開させる
    video_capture.open(0)
    ret, frame = video_capture.read()
    if not ret:
        break

    #画像処理を早くするために画像の大きさを4分の1の大きさにする
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    
    #取得したライブ映像に写っている顔の位置を取得する
    face_locations = face_recognition.face_locations(small_frame)
    #映像の顔の特徴を取得する
    unknown_encodings = face_recognition.face_encodings(small_frame, face_locations)
    
    
    face_names = []
    for unknown_encoding in unknown_encodings:
        #顔の特徴を比べる
        result = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
        
        if True in result:
            #モータ制御をするために画像処理を一時停止
            video_capture.release()
            first_match = result.index(True)
            #マッチした人の名前を取り出す
            name = known_face_names[first_match]
            
            #モータを回す（鍵を開ける） 
            servo.ChangeDutyCycle(2.5)
            time.sleep(5)

            servo.ChangeDutyCycle(7.25)
            time.sleep(0.5)

            servo.ChangeDutyCycle(0)



        else:
            #顔の特徴が一致するものがない場合、unknownと表示する
            name = "unknown"
        face_names.append(name)
    #第1引数にライブ映像、第2引数に顔の位置、第3引数に人の名前のリストを渡す    
    boxes(frame, face_locations, face_names)
    
    #キーボードがされると繰り返しから抜ける
    #押されていない状態で−1が帰っくる
    if cv2.waitKey(1) != -1:
        print("key pressed")
        break

video_capture.release()
cv2.destroyAllWindows()
servo.stop()
GPIO.cleanup()
