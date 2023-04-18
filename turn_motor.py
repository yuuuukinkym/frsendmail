# %%
#GIOP用のモジュールと時間制御用のモジュールをインポート
import RPi.GPIO as GPIO
import time

# %%
#ポート番号を定義
gp_out = 4
#GPIOの設定
GPIO.setmode(GPIO.BCM)  #GPIOのモードをGPIO.BCMに設定
GPIO.setup(gp_out, GPIO.OUT)    #GPIO4を出力モードに設定

# %%
#PWMの設定
#サーボモータSG90の周波数は、50Hz 
servo = GPIO.PWM(gp_out, 50)
servo.start(0)

# %%
for i in range(3):
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    servo.ChangeDutyCycle(12)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

servo.stop()
GPIO.cleanup()

# %%



