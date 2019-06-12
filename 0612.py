import os
import time

import cv2.cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

#圖片資料夾
dir_path = os.path.join(os.getcwd(), 'pic')  #path相加 中間有\

#定義固定參數
TOP = 40 #標題預留空間
WIDTH, HEIGHT = 320, 180  #圖片顯示比例
demo_height, demo_width = [3 * (HEIGHT + TOP) + TOP, 3 * (WIDTH)]#顯示範圍 最多可以讀到9張圖片

#用以圖片預覽 固定顯示範圍
canvas = np.ones((demo_height, demo_width, 3), dtype=np.uint8) * 0

#選擇檔案
def _select():
    #找目錄中圖片 同時製作縮圖
    images_path = []
    files = os.listdir(dir_path) #從目錄取得所有檔名
    for f in files:
        if os.path.splitext(f)[-1] in ['.jpg', '.png']:#分離副檔名
            images_path.append(os.path.join(dir_path, f))
    #清空畫布
    canvas = np.ones((demo_height, demo_width, 3), dtype=np.uint8) * 0
    #製作縮圖 同時加入到畫布供選擇
    for counter, img_path in enumerate(images_path):
        img = cv.imread(img_path)
        img_temp = cv.resize(img, (WIDTH, HEIGHT), interpolation=cv.INTER_CUBIC)
        #插入圖片定位點 由上至下為:留黑+標題+圖片+標題+圖片+標題+圖片
        t = TOP + int(counter / 3) * (TOP + HEIGHT)
        d = (TOP + HEIGHT) * int(counter / 3 + 1)
        l = (counter % 3) * WIDTH
        r = (counter % 3 + 1) * WIDTH
        #插入圖片到定位點
        canvas[TOP + t:TOP + d, l:r] = img_temp
        _myprint(canvas, str(counter), int(l + WIDTH / 2), TOP + t)
    while 1:
        _myprint(canvas, "Select pic 0 ~ {} or Press 'q' to exit.".format(len(images_path) - 1))
        cv.imshow('My Image', canvas)
        ch = cv.waitKey(0)
        #輸入數字判斷
        nums = [ord(str(i)) for i in range(len(images_path))]
        if ch in [ord('q'), ord('Q')]:
            cv.destroyAllWindows()
            break
        else:
            for c, i in enumerate(nums):
                if ch == i:
                    cv.destroyAllWindows()
                    image_path = images_path[c]
                    return cv.imread(image_path)

#圖片處理
def _revision(img):
    #清空畫布
    canvas = np.ones((demo_height, demo_width, 3), dtype=np.uint8)
    l = 1#亮度
    r = 1#紅色
    g = 1#綠色
    b = 1#藍色
    c = 1#對比度
    #建立副本 之後所有操作都會在副本上執行 最後才進行存檔
    img_copy = cv.resize(img, (WIDTH * 3, HEIGHT * 3), interpolation=cv.INTER_CUBIC)
    while 1:
        _clear(canvas)
        _myprint(canvas, 'Index : [L brightness], [C Contrast]')
        canvas[4 * TOP:TOP + (TOP + HEIGHT) * 3,:] = img_copy
        cv.imshow('My Image', canvas)
        ch = cv.waitKey(0)
        if ch in [ord('q'), ord('Q')]:
            cv.destroyAllWindows()
            break
        elif ch in [ord('c'), ord('C')]:
            black = np.zeros([HEIGHT * 3, WIDTH * 3, 3], img_copy.dtype)
            img_temp = img_copy#用來預覽的副本
            while 1:
                _myprint(canvas, 'Picture brightness', y=40)
                canvas[4 * TOP:TOP + (TOP + HEIGHT) * 3,:] = img_temp
                cv.imshow('My Image', canvas)
                ch = cv.waitKey(0)
                print(c)
                if ch == ord('+'):
                    c += 0.01
                elif ch == ord('-'):
                    c -= 0.01
                elif ch in [ord('s'), ord('S')]:
                    img_copy = img_temp
                    break
                elif ch in [ord('q'), ord('Q')]:
                    break
                img_temp = cv.addWeighted(img_copy, c, black, 1 - c, 0)
        elif ch in [ord('l'), ord('L')]:
            black = np.zeros([HEIGHT * 3, WIDTH * 3, 3], img_copy.dtype)
            img_temp = img_copy  #用來預覽的副本
            while 1:
                print(1)  
        else:
            print("Press 'q' to exit.")

def _clear(canvas, t = 0, d = 40 * 3, l = 0, r = demo_width):
    canvas[t:d, l:r] = 0
def _myprint(canvas, text, x = 0, y = 40):
    cv.putText(canvas, text, (int(x), y), cv.FONT_HERSHEY_DUPLEX, 1, [255, 255, 255])
img = _select()
_revision(img)