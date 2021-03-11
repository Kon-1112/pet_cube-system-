import time
import RPi.GPIO as GPIO

#自動餌やり機能の制御プログラム
def servo(timer):
    #出力ピンの指定
    servo_pin = 4
    #GPIO初期化
    GPIO.setmode(GPIO.BCM)
    #GPIOを出力に設定
    GPIO.setup(servo_pin,GPIO.OUT)
    #PWM制御の設定（50Hz）
    Servo = GPIO.PWM(servo_pin,50)
    #初期値に移動
    Servo.start(0)
    #度数に変換する関数
    def servo_angle(angle):
        duty = 2.5+(12.0-2.5)*(angle+90)/180
        Servo.ChangeDutyCycle(duty)
    #餌やり弁を開く
    servo_angle(90)
    #サーボモータの処理待機
    time.sleep(timer)
    #餌やり弁を閉じる
    servo_angle(-90)
    #サーボモータの処理待機
    time.sleep(0.6)
if __name__=='__main__':
    servo(timer)
    
