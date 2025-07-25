#! /usr/bin/python
# headshots.py

"""
2025/07/25  usbカメラ仕様に変更した
"""
import os
import sys
import cv2
import config

name = input("あなたの名前をローマ字で登録してください: ")
try:
    userDirPath = "dataset/" + name
    os.mkdir(userDirPath)
except:
    print("Datasets already exist.")
    sys.exit()

# カメラタイプの取り込み（※ USBカメラでは不要だけど残してOK）
camera_type  = config.camera_type()
# カメラから取り込む画像の大きさの設定
camera_width_x , camera_width_y  = config.camera_width()
# 処理用の画像の大きさの設定
proces_width_x , proces_width_y  = config.proces_width()

# USBカメラを初期化
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width_x)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_width_y)

# USBカメラが開けたか確認
if not cap.isOpened():
    print("カメラが開けません")
    sys.exit()

cv2.namedWindow("スペースを押して写真を保存", cv2.WINDOW_NORMAL)
cv2.resizeWindow("スペースを押して写真を保存", proces_width_x, proces_width_y)

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("カメラからフレームを取得できませんでした")
        break

    cv2.imshow("スペースを押して写真を保存", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27 or k % 256 == 113:  # ESC or q
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:  # Space
        img_name = f"dataset/{name}/image_{img_counter}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"{img_name} written!")
        img_counter += 1

cap.release()
cv2.destroyAllWindows()
