import requests
import argparse
import camera
#LINE送信プログラム
def line(message,image):
    def lineNotify(message,args):
        line_notify_api = ''
        line_notify_token = ''
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        #メッセージのみの送信
        if len(args) == 0:
            requests.post(line_notify_api, data=payload, headers=headers)
        #画像つきの送信
        else:
            files={"imageFile":open(args,"rb")}
            requests.post(line_notify_api, data=payload, headers=headers,files=files)
    #画像が必要か不要かを判断
    if image == True:
        image_url ="picture_data.jpg"
    else:
        image_url =""
    lineNotify(message,image_url)
    
if __name__=='__main__':
    camera.camera()
    line(message,image)
