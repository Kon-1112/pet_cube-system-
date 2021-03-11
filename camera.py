import cv2
#撮影用カメラの制御プログラム
def camera():    
    cc = cv2.VideoCapture(0)
    rr,img = cc.read()
    cv2.imwrite('picture_data'+'.jpg',img)
    cc.release()
if __name__ == '__main__':
    camera()
