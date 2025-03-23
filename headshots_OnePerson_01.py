#! /usr/bin/python
# headshots.py

"""
2025/03/08  Bullseyeへ変換
            終了はecs
2025/03/11  画像サイズをconfigで設定
"""
import os
import sys
import cv2
from picamera2 import Picamera2
import config

name = input("あなたの名前をローマ字で登録してください: ")
try:
    userDirPath = "dataset/" + name
    os.mkdir(userDirPath)
except:
    print("Datasets already exist.")
    sys.exit()

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
