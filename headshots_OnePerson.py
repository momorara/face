#! /usr/bin/python
# headshots.py

"""
2025/03/08  Bullseyeへ変換
            終了はecs
2025/03/11  画像サイズをconfigで設定
2025/03/30  組み合わせテスト 
2025/07/25  カメラタイプ対応 *1
2025/12/27  デフォルトv3対応 エラーでv1.3になる
2026/01/18  名前の文字列の先頭にある空白を削除する

headshots_OnePerson_01.py
    パイカメラv1.3を使い一人分の顔写真を撮影する。
    プログラムを起動すると名前を聞いてくるので、入力すると撮影モードになる(名前は半角英数字のみ)
    スペースキーでシャッターを切る
    ESCかqキーが押されたらプログラム終了
"""
import os
import sys
import cv2
from   picamera2 import Picamera2
import config
# *1
from libcamera import controls

name = input("あなたの名前をローマ字で登録してください: ")
name = name.lstrip()
try:
    userDirPath = "dataset/" + name
    os.mkdir(userDirPath)
except:
    print("Datasets already exist.")
    sys.exit()

# カメラタイプの取り込み *1
camera_type  = config.camera_type()
# カメラから取り込む画像の大きさの設定
camera_width_x , camera_width_y  = config.camera_width()
# 処理用の画像の大きさの設定
proces_width_x , proces_width_y  = config.proces_width()

# Picamera2 を使用
picam2 = Picamera2()
# config = picam2.create_preview_configuration(main={"size": (640, 480)})
# 色がおかしかったので、修正
config = picam2.create_preview_configuration(main={"size": (camera_width_x, camera_width_y), "format": "RGB888"})
picam2.configure(config)
if camera_type == 3:
    # オートフォーカスを有効にする *1
    try:
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    except:
        pass
picam2.start()

cv2.namedWindow("スペースを押して写真を保存", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("press space to take a photo", 500, 300)
cv2.resizeWindow("スペースを押して写真を保存", proces_width_x, proces_width_y)

img_counter = 0

while True:
    frame = picam2.capture_array()
    # frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)
    cv2.imshow("スペースを押して写真を保存", frame)

    k = cv2.waitKey(1)
    if k%256 == 27 or k%256 == 113: #ESCかqキーが押されたら終了
        # ESCキーが押されたら終了
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # スペースキーが押されたら写真を保存
        img_name = f"dataset/{name}/image_{img_counter}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"{img_name} written!")
        img_counter += 1

cv2.destroyAllWindows()
