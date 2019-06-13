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
        #只取9張圖
        if counter == 9:
            break
        img = cv.imread(img_path)
        img_temp = cv.resize(img, (WIDTH, HEIGHT), interpolation=cv.INTER_CUBIC)
        #插入圖片定位點 由上至下為:留黑+標題+圖片+標題+圖片+標題+圖片
        t = TOP + int(counter / 3) * (TOP + HEIGHT)
        d = (TOP + HEIGHT) * int(counter / 3 + 1)
        l = (counter % 3) * WIDTH
        r = (counter % 3 + 1) * WIDTH
        #插入圖片到定位點
        canvas[TOP + t:TOP + d, l:r] = img_temp
        _myprint(canvas, str(counter), int(l + WIDTH / 2), TOP + t, 0)#最後一個參數 不clear畫面
    while 1:
        _myprint(canvas, "Select pic 0 ~ {} or Press 'q' to exit.".format(len(images_path) - 1))
        cv.imshow('My Image', canvas)
        ch = cv.waitKey(0)
        #輸入數字判斷
        nums = [ord(str(i)) for i in range(len(images_path))]
        if ch in [ord('q'), ord('Q')]:
            cv.destroyAllWindows()
            return 0
        else:
            for c, i in enumerate(nums):
                if ch == i:
                    cv.destroyAllWindows()
                    image_path = images_path[c]
                    return image_path
#圖片處理
def _revision(img):
    #清空畫布
    canvas = np.ones((demo_height, demo_width, 3), dtype=np.uint8)
    #影像處理步驟
    revision = []
    #建立副本 之後所有操作都會以副本為標準執行 最後才進行存檔
    img_copy = cv.resize(img.copy(), (WIDTH * 3, HEIGHT * 3), interpolation=cv.INTER_CUBIC)
    while 1:
        #自定義的用來處理canvas的函式 clear沒有引數則全清空 myprint用來印出一行
        _clear(canvas)
        _myprint(canvas, 'KEY : [(Q)uit], [(U)ndo], [(S)ave]')
        _myprint(canvas, '      [(L)ightness], [(C)ontrast]', y=2 * TOP)
        #revision用來記錄以往的所有處理 方便使用UNDO刪除
        _myprint(canvas, str(revision), y=3 * TOP)
        #make用來進行以往的所有處理 希望可以將每個處理記錄下來 所以才使用此方法
        img_temp = _make(revision, img_copy)
        canvas[4 * TOP:TOP + (TOP + HEIGHT) * 3,:] = img_temp
        cv.imshow('My Image', canvas)
        ch = cv.waitKey(0)
        if ch in [ord('q'), ord('Q')]:
            cv.destroyAllWindows()
            return 0
        elif ch in [ord('s'), ord('S')]:
            img = _make(revision, img)
            return img
        elif ch in [ord('u'), ord('U')]:
            if len(revision) > 0:
                del revision[-1]
        elif ch in [ord('c'), ord('C')]:
            c = _contrast(canvas, img_temp.copy())
            if isinstance(c, tuple):
                revision.append(c)#return對比度
        elif ch in [ord('l'), ord('L')]:
            l = _lightness(canvas, img_temp.copy())
            if isinstance(l, tuple):
                revision.append(l)#return對比度
#清除畫布上方黑板用
def _clear(canvas, t = 0, d = TOP * 4, l = 0, r = demo_width):
    canvas[t:d, l:r] = 0
#畫布上方黑板上印字
def _myprint(canvas, text, x=0, y=TOP, clear=True):
    if clear == True:
        canvas[y - TOP:y, :] = 0
    cv.putText(canvas, text, (int(x), y), cv.FONT_HERSHEY_DUPLEX, 1, [255, 255, 255])
#對比度調整 每次作業只變更變數C與緩存圖片 程式最後才會對原圖進行影響
def _contrast(canvas, img):
    c = 1
    black = np.zeros([HEIGHT * 3, WIDTH * 3, 3], img.dtype)
    img_temp = img
    while 1:
        _myprint(canvas, 'Picture contrast', y=40)
        _myprint(canvas, 'Contrast = {:.2f}'.format(c), y=80)
        _myprint(canvas, 'KEY : [(Q)uit], [(S)ave], [-], [+]', y=120)
        canvas[4 * TOP:TOP + (TOP + HEIGHT) * 3,:] = img_temp
        cv.imshow('My Image', canvas)
        ch = cv.waitKey(0)
        if ch == ord('+'):
            c += 0.01
        elif ch == ord('-'):
            c -= 0.01
        elif ch in [ord('s'), ord('S')]:
            return ('C', c)#包成封包回傳給主函式
        elif ch in [ord('q'), ord('Q')]:
            break
        #圖片合成函式 C代表比重
        img_temp = cv.addWeighted(img, c, black, 1 - c, 0)
#亮度調整 每次作業只變更變數C與緩存圖片 程式最後才會對原圖進行影響
def _lightness(canvas, img):
    l = 1
    black = np.zeros([HEIGHT * 3, WIDTH * 3, 3], img.dtype)
    img_temp = img
    while 1:
        _myprint(canvas, 'Picture lightness', y=40)
        _myprint(canvas, 'Lightness = {:.2f}'.format(l), y=80)
        _myprint(canvas, 'KEY : [(Q)uit], [(S)ave], [-], [+]', y=120)
        canvas[4 * TOP:TOP + (TOP + HEIGHT) * 3,:] = img_temp
        cv.imshow('My Image', canvas)
        ch = cv.waitKey(0)
        if ch == ord('+'):
            l += 1
        elif ch == ord('-'):
            l -= 1
        elif ch in [ord('s'), ord('S')]:
            return ('L', l)#包成封包回傳給主函式
        elif ch in [ord('q'), ord('Q')]:
            break
        #圖片合成函式 l代表亮度
        img_temp = cv.addWeighted(img, 1, black, 0, l)
#相圖片依照傳來的封包進行處理
def _make(r, img):
    black = np.zeros(img.shape, img.dtype)
    for i in r:
        if i[0] == 'C':
            img = cv.addWeighted(img, i[1], black, 1 - i[1], 0)
        elif i[0] == 'L':
            img = cv.addWeighted(img, 1, black, 0, i[1])
    return img
img_path = ''
while not isinstance(img_path, int):
    #選擇圖片 回傳路徑
    img_path = _select()
    if not isinstance(img_path, int):
        #讀取圖片
        img = cv.imread(img_path)
        #製作圖片 回傳圖片
        newimg = _revision(img)
        #存檔動作
        if not isinstance(newimg, int):
            #新檔名後方增加日期時間
            filepath = os.path.splitext(img_path)[0] + time.strftime('_%m-%d_%H-%M-%S') + '.jpg'
            #存檔
            print('save as "{}"'.format(filepath))
            cv.imwrite(filepath, newimg)