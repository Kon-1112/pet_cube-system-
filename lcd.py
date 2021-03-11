import HD44780 as LCD
import RPi.GPIO as GPIO
import time
import app

def lcd(mainalert,subalert,message_1,message_2):
    lcd = LCD.HD44780('lcdsample.conf')
    lcd.init()
    lcd.message(f'{mainalert}',1)
    lcd.message(f'{subalert}',2)
    lcd.message(f'{message_1}',3)
    lcd.message(f'{message_2}',4)
if __name__=='__main__':
    lcd(mainalert,subalert,message_1,message_2)
    