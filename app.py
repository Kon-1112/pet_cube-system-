from flask import Flask,render_template,request
import servo
import line
import lcd
import time
import camera
import datetime
import psycopg2

app = Flask(__name__)
dt_login = datetime.datetime.now()
login_time = dt_login.strftime('%Y年%m月%d日 %H:%M:%S')

def user_check(name,password):
    users = 'postgres'
    dbnames = 'pet_cube'
    passwords = 'pass'

    conn = psycopg2.connect('postgresql://admin:pass@localhost:5432/pet_cube')
    sql_user=(f"SELECT * FROM user_data WHERE name='{name}' and password='{password}';")
   
    sql_user_check = conn.cursor()
    sql_user_check.execute(sql_user)
    results = sql_user_check.fetchall()
    if len(results)==0:
        check = '登録されていないか、入力内容に誤りがございます。'
    else:
        check = '認証成功'
        print(f"{name}さんようこそ！")
    print(f"\n{results}")
    sql_user_check.close()
    conn.close()
    return(check)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home',methods=['POST'])
def home():
    lcd.lcd('      PowerON','   Web connected','          ','')
    return render_template('home.html',login_time=login_time)


@app.route('/now_room',methods=['POST'])
def now_room():
    line_pref = str(request.form.get('line'))
    camera.camera()
    lcd.lcd('      PowerON','   Web connected','NOW ROOM','')
    title = 'Now my room'
    if line_pref =='On':
        line.line(title,True)
    else:
        camera.camera()
    return render_template('now.html',title=title)

@app.route('/send_message',methods=["POST"])
def send_message():
    message = str(request.form.get('msg'))
    line.line(message,False)
    dt_now = datetime.datetime.now()
    message = dt_now.strftime('%m月%d日 %H:%M') +'に「'+message+'」を送信しました！'
    lcd_msg = 'Send Message'
    lcd.lcd('      PowerOn','   Web connected','メッセーゾヲソウシンシマシアタ','')
    return render_template('home.html',msg_log=message,login_time=login_time)

@app.route('/servo_move',methods=["POST"])
def servo_move():
    feed = str(request.form.get('feed'))
    if feed == 'many':
        lcd.lcd('      PowerOn','   Web connected','MANY','')
        servo.servo(1)
        feed="多めに"
    elif feed == 'usually':
        lcd.lcd('      PowerOn','   Web connected','USUALLY','')
        servo.servo(0.8)
        feed="普通に"
    else:
        lcd.lcd('      PowerOn','   Web connected','LESS','')
        servo.servo(0.5)
        feed='少なめに'
        
    time.sleep(1)
    dt_now = datetime.datetime.now()
    log_msg = dt_now.strftime('%m月%d日 %H:%M') +'に餌を'+feed+'与えました！'
    lcd.lcd('      PowerON','   Web connected','','')
    return render_template('home.html',servo_log=log_msg,login_time=login_time)

if __name__=="__main__":
    app.run(debug=True,port=0000)
